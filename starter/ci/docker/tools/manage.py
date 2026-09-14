"""Local classroom CI setup. Runs inside Compose, never edits /source."""
import argparse
import base64
import http.cookiejar
import io
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import zipfile

STATE = Path('/state')
SOURCE = Path('/source')
PROJECT = os.environ.get('CI_PROJECT', 'tdd-bdd-classroom')
NETWORK = os.environ.get('CI_NETWORK', PROJECT + '-ci')
GL = 'http://gitlab:18781'
JK = 'http://jenkins:8080'
PUBLIC_GL = 'http://127.0.0.1:' + os.environ.get('CI_GITLAB_PORT', '18781')
PUBLIC_JK = 'http://127.0.0.1:' + os.environ.get('CI_JENKINS_PORT', '18780')
REPLACEMENTS = {
    'TODO_PYTEST_COMMAND': 'python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml',
    'TODO_PYTEST_XML': 'reports/pytest.xml',
    'TODO_BEHAVE_COMMAND': 'python -m behave --tags="not @wip" --junit --junit-directory reports/behave',
    'TODO_BEHAVE_XML': 'reports/behave/*.xml',
}
OPENER = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
CRUMB = {}


def save(name, value):
    path = STATE / name
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')
    path.chmod(0o600)


def load(name):
    return json.loads((STATE / name).read_text(encoding='utf-8'))


def secret(name):
    return (STATE / name).read_text(encoding='utf-8').strip()


def init():
    STATE.mkdir(parents=True, exist_ok=True)
    for name in ('gitlab-password', 'jenkins-password', 'gitlab-api-token'):
        path = STATE / name
        if not path.exists():
            path.write_text(secrets.token_urlsafe(32), encoding='utf-8')
            # GitLab's git user needs read access in the container-only volume.
            path.chmod(0o644)
    print('Lokale Zugangsdaten bereit. Vorhandene Passwörter bleiben erhalten.')


def request(url, method='GET', data=None, headers=None, raw=False):
    headers = dict(headers or {})
    if isinstance(data, dict):
        data = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with OPENER.open(req, timeout=90) as response:
            body = response.read()
    except urllib.error.HTTPError as exc:
        # Do not echo API responses: these may contain authentication material.
        raise RuntimeError(f'{method} {urllib.parse.urlsplit(url).path}: HTTP {exc.code}') from None
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        raise RuntimeError(f'{urllib.parse.urlsplit(url).netloc} noch nicht erreichbar ({type(exc).__name__}).') from None
    return body if raw else json.loads(body or b'{}')


def gl(path, method='GET', data=None, raw=False):
    return request(GL + '/api/v4' + path, method, data, {'PRIVATE-TOKEN': secret('gitlab-api-token')}, raw)


def jk(path, method='GET', data=None, content_type=None, raw=False):
    auth = base64.b64encode(('seminar:' + secret('jenkins-password')).encode()).decode()
    headers = {'Authorization': 'Basic ' + auth}
    if method != 'GET':
        if not CRUMB:
            crumb = jk('/crumbIssuer/api/json')
            CRUMB[crumb['crumbRequestField']] = crumb['crumb']
        headers.update(CRUMB)
    if content_type:
        headers['Content-Type'] = content_type
    return request(JK + path, method, data, headers, raw)


def docker(*args):
    result = subprocess.run(['docker', *args], capture_output=True, text=True, timeout=240)
    if result.returncode:
        raise RuntimeError('Docker-Aufruf fehlgeschlagen: ' + ' '.join(args[:2]) + '. Dienste mit docker compose ... ps prüfen.')
    return result.stdout.strip()


def container(service):
    ids = docker('ps', '-q', '--filter', 'label=com.docker.compose.project=' + PROJECT,
                 '--filter', 'label=com.docker.compose.service=' + service).splitlines()
    if len(ids) != 1:
        raise RuntimeError(f'Dienst {service} läuft nicht eindeutig. Zuerst docker compose -f docker/compose.yaml up -d --build ausführen.')
    return ids[0]


def wait_for(label, check, seconds=1200):
    deadline = time.monotonic() + seconds
    last = ''
    while time.monotonic() < deadline:
        try:
            value = check()
            if value:
                return value
        except RuntimeError as exc:
            last = str(exc)
        print(label + ' …', flush=True)
        time.sleep(10)
    raise RuntimeError(f'Zeitlimit: {label}. {last} Dienste und Docker-Ressourcen prüfen; Befehl danach wiederholen.')


def configure():
    init()
    wait_for('Warte auf GitLab (beim ersten Start mehrere Minuten)',
             lambda: request(GL + '/users/sign_in', raw=True))
    wait_for('Warte auf Jenkins und Plugins', lambda: jk('/api/json'))
    bootstrap = STATE / 'bootstrap.rb'
    bootstrap.write_text('''user = User.find_by_username!("root")
token = user.personal_access_tokens.find_or_initialize_by(name: "classroom-local-api")
token.scopes = ["api"]
token.expires_at = 7.days.from_now.to_date
token.revoked = false
token.set_token(File.read("/state/gitlab-api-token").strip)
token.save!
ApplicationSetting.current.update!(signup_enabled: false)
''', encoding='utf-8')
    bootstrap.chmod(0o644)
    print('Richte lokales GitLab-Projekt und Projekt-Runner ein …')
    docker('exec', container('gitlab'), 'gitlab-rails', 'runner', '/state/bootstrap.rb')
    projects = gl('/projects?owned=true&search=rabattshop&per_page=100')
    project = next((p for p in projects if p['path_with_namespace'] == 'root/rabattshop'), None)
    if project is None:
        project = gl('/projects', 'POST', {'name': 'Rabattshop', 'path': 'rabattshop',
                                          'visibility': 'public', 'initialize_with_readme': False})
    pid = project['id']
    save('project.json', {'id': pid})
    runners = gl(f'/projects/{pid}/runners')
    owned = next((r for r in runners if r['description'] == 'Classroom Docker runner'), None)
    if owned is None:
        runner = gl('/user/runners', 'POST', {'runner_type': 'project_type', 'project_id': pid,
                                            'description': 'Classroom Docker runner', 'run_untagged': True})
        save('runner.json', {'id': runner['id'], 'token': runner['token']})
    elif not (STATE / 'runner.json').exists() or load('runner.json')['id'] != owned['id']:
        raise RuntimeError('Runner vorhanden, aber lokaler Token fehlt. Keine weiteren Runner angelegt; siehe README zur vollständigen Neueinrichtung.')
    config = f'''concurrent = 2
check_interval = 3
[[runners]]
  name = "Classroom Docker runner"
  url = "{GL}"
  clone_url = "{GL}"
  token = {json.dumps(load('runner.json')['token'])}
  executor = "docker"
  [runners.docker]
    image = "python:3.12"
    privileged = false
    network_mode = "{NETWORK}"
    volumes = ["/cache"]
'''
    Path('/runner-config/config.toml').write_text(config, encoding='utf-8')
    Path('/runner-config/config.toml').chmod(0o600)
    docker('restart', container('runner'))
    wait_for('Warte auf die Runner-Verbindung',
             lambda: any(r.get('status') == 'online' for r in gl(f'/projects/{pid}/runners')), 180)
    print('Einrichtung abgeschlossen. Jetzt: docker compose -f docker/compose.yaml run --rm setup run')
    print('Zugangsdaten: docker compose -f docker/compose.yaml run --rm setup credentials')


def snapshot(source, demo=False, case='green'):
    files = {}
    required = ('.gitlab-ci.yml', 'Jenkinsfile', 'requirements.txt', 'pyproject.toml', 'behave.ini')
    for name in required:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise RuntimeError('Im Übungsordner fehlt: ' + name)
        files[name] = path.read_text(encoding='utf-8-sig')
    for folder in ('src', 'tests', 'features', 'scripts'):
        root = source / folder
        if root.is_symlink():
            raise RuntimeError('Quellordner darf kein symbolischer Link sein: ' + folder)
        for path in sorted(root.rglob('*')):
            rel = path.relative_to(source)
            if any(part.startswith('.') or part == '__pycache__' for part in rel.parts):
                continue
            if any(source.joinpath(*rel.parts[:i]).is_symlink() for i in range(1, len(rel.parts) + 1)):
                continue
            if path.is_file() and (path.suffix in ('.py', '.feature') or path.name.endswith('.approved.txt')):
                files[rel.as_posix()] = path.read_text(encoding='utf-8-sig')
    for name in ('.gitlab-ci.yml', 'Jenkinsfile'):
        if demo:
            for old, new in REPLACEMENTS.items():
                files[name] = files[name].replace(old, new)
        if 'TODO_' in files[name]:
            raise RuntimeError(f'{name} enthält noch TODOs. Erst die vier Platzhalter ergänzen; für einen Funktionstest run --demo verwenden.')
    if case == 'unit-red':
        files['tests/test_ci_probe.py'] = 'def test_ci_probe():\n    assert False, "Absichtlicher CI-Testfehler"\n'
    elif case == 'bdd-red':
        files['features/ci_probe.feature'] = '# language: de\nFunktionalität: CI-Probe\n  Szenario: Fehler berichten\n    Dann ist die CI-Probe absichtlich rot\n'
        files['features/steps/ci_probe.py'] = 'from behave import then\n\n@then("ist die CI-Probe absichtlich rot")\ndef ci_probe(context):\n    assert False, "Absichtlicher BDD-Testfehler"\n'
    elif case == 'coverage-low':
        files['src/shop/ci_uncovered.py'] = 'def unused(value):\n' + ''.join(
            f'    if value == {i}:\n        return {i}\n' for i in range(200)) + '    return None\n'
    return files


def lint(pid, files):
    result = gl(f'/projects/{pid}/ci/lint', 'POST', {'content': files['.gitlab-ci.yml']})
    if not result['valid']:
        raise RuntimeError('GitLab-Pipeline ungültig: ' + '; '.join(result.get('errors', [])))
    boundary = 'classroom-' + secrets.token_hex(12)
    data = (f'--{boundary}\r\nContent-Disposition: form-data; name="jenkinsfile"\r\n'
            f'Content-Type: text/plain\r\n\r\n{files["Jenkinsfile"]}\r\n--{boundary}--\r\n').encode()
    result = jk('/pipeline-model-converter/validate', 'POST', data, 'multipart/form-data; boundary=' + boundary, True).decode()
    if 'successfully validated' not in result:
        raise RuntimeError('Jenkinsfile ungültig: ' + result[:2000])
    print('Beide Server akzeptieren die Pipeline-Dateien.')


def commit_snapshot(pid, branch, files):
    branches = {b['name'] for b in gl(f'/projects/{pid}/repository/branches?per_page=100')}
    base = branch if branch in branches else ('main' if 'main' in branches else next(iter(sorted(branches)), None))
    old = set()
    if base:
        page = 1
        while True:
            entries = gl(f'/projects/{pid}/repository/tree?recursive=true&per_page=100&page={page}&ref={base}')
            old.update(e['path'] for e in entries if e['type'] == 'blob')
            if len(entries) < 100:
                break
            page += 1
    actions = [{'action': 'update' if path in old else 'create', 'file_path': path,
                'content': content} for path, content in sorted(files.items())]
    actions += [{'action': 'delete', 'file_path': path} for path in sorted(old - files.keys())]
    data = {'branch': branch, 'commit_message': 'CI exercise: ' + branch, 'actions': actions}
    if branch not in branches and base:
        data['start_branch'] = base
    sha = gl(f'/projects/{pid}/repository/commits', 'POST', data)['id']
    if branch == 'main':
        gl(f'/projects/{pid}', 'PUT', {'default_branch': 'main'})
    return sha


def start_jenkins(name, sha):
    xml = f'''<flow-definition plugin="workflow-job">
<description>Seminar: derselbe Commit wie in GitLab ({sha})</description>
<keepDependencies>false</keepDependencies><properties><org.jenkinsci.plugins.workflow.job.properties.DisableConcurrentBuildsJobProperty/></properties>
<definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
<scm class="hudson.plugins.git.GitSCM" plugin="git"><configVersion>2</configVersion>
<userRemoteConfigs><hudson.plugins.git.UserRemoteConfig><url>{GL}/root/rabattshop.git</url></hudson.plugins.git.UserRemoteConfig></userRemoteConfigs>
<branches><hudson.plugins.git.BranchSpec><name>{escape(sha)}</name></hudson.plugins.git.BranchSpec></branches>
<doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations><submoduleCfg class="empty-list"/>
<extensions><hudson.plugins.git.extensions.impl.CleanBeforeCheckout/></extensions></scm>
<scriptPath>Jenkinsfile</scriptPath><lightweight>false</lightweight></definition><triggers/><disabled>false</disabled></flow-definition>'''
    jobs = jk('/api/json?tree=jobs[name]')['jobs']
    path = f'/job/{name}/config.xml' if any(j['name'] == name for j in jobs) else '/createItem?name=' + name
    jk(path, 'POST', xml.encode(), 'application/xml', True)
    number = jk(f'/job/{name}/api/json')['nextBuildNumber']
    jk(f'/job/{name}/build', 'POST', b'', raw=True)
    return number


def xml_summary(xmls):
    result = {}
    for name, data in sorted(xmls.items()):
        root = ET.fromstring(data)
        if name.endswith('/coverage.xml'):
            result[name] = {k: float(root.attrib[k]) for k in ('line-rate', 'branch-rate')}
        else:
            suites = [root] if root.tag == 'testsuite' else list(root.iter('testsuite'))
            result[name] = {k: sum(int(s.attrib.get(k, 0)) for s in suites)
                            for k in ('tests', 'failures', 'errors', 'skipped')}
    return result


def collect(pid, pipeline, name, number, case, sha):
    jobs = gl(f'/projects/{pid}/pipelines/{pipeline}/jobs')
    gl_xml = {}
    for job in jobs:
        if job.get('artifacts_file', {}).get('filename'):
            data = gl(f'/projects/{pid}/jobs/{job["id"]}/artifacts', raw=True)
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for path in archive.namelist():
                    if path.startswith('reports/') and path.endswith('.xml'):
                        gl_xml[path] = archive.read(path)
    build = jk(f'/job/{name}/{number}/api/json')
    revisions = {a['lastBuiltRevision']['SHA1'] for a in build['actions'] if a.get('lastBuiltRevision')}
    if revisions != {sha}:
        raise RuntimeError('Jenkins hat nicht den erwarteten Commit ausgecheckt.')
    jk_xml = {a['relativePath']: jk(f'/job/{name}/{number}/artifact/' + urllib.parse.quote(a['relativePath']), raw=True)
              for a in build['artifacts'] if a['relativePath'].startswith('reports/') and a['relativePath'].endswith('.xml')}
    summary = {'gitlab': xml_summary(gl_xml), 'jenkins': xml_summary(jk_xml),
               'gitlab_jobs': {j['name']: j['status'] for j in jobs},
               'jenkins_stages': jk(f'/job/{name}/{number}/wfapi/describe')['stages']}
    if case == 'unit-red':
        console = jk(f'/job/{name}/{number}/consoleText', raw=True).decode(errors='replace')
        # wfapi reports FAILED for skipped stages too; use the explicit skip evidence.
        summary['jenkins_bdd_skipped'] = 'Stage "BDD tests (behave)" skipped due to earlier failure(s)' in console
    save(name + '-reports.json', summary)
    for label, reports in (('GitLab', summary['gitlab']), ('Jenkins', summary['jenkins'])):
        required = {'reports/pytest.xml', 'reports/coverage.xml'}
        if label == 'GitLab' or case != 'unit-red':
            required |= {'reports/behave/TESTS-rabatt.xml', 'reports/behave/TESTS-coupon.xml'}
        if not required <= reports.keys():
            raise RuntimeError(label + ': Berichte fehlen: ' + ', '.join(sorted(required - reports.keys())))
        for path, values in reports.items():
            print(label, path + ':', ', '.join(f'{k}={v}' for k, v in values.items()))
        failures = sum(r.get('failures', 0) + r.get('errors', 0) for r in reports.values())
        expected_failures = 1 if case in ('unit-red', 'bdd-red') else 0
        if failures != expected_failures:
            raise RuntimeError(label + ': Testberichte passen nicht zum gewählten Vergleichsfall.')
        if any(r.get('tests') == 0 for r in reports.values()):
            raise RuntimeError(label + ': Ein JUnit-Bericht enthält keine Testfälle.')
        if case == 'coverage-low':
            coverage = reports['reports/coverage.xml']
            if coverage['line-rate'] >= .60 or coverage['branch-rate'] >= .50:
                raise RuntimeError(label + ': Die Coverage unterschreitet nicht beide vorgesehenen Grenzwerte.')
    for path in summary['gitlab'].keys() & summary['jenkins'].keys():
        if summary['gitlab'][path] != summary['jenkins'][path]:
            raise RuntimeError('Unterschiedliche Test- oder Coverage-Ergebnisse: ' + path)
    if case == 'unit-red':
        if summary['gitlab_jobs'].get('behave') != 'success':
            raise RuntimeError('GitLab: behave sollte trotz rotem pytest-Job erfolgreich laufen.')
        if not summary['jenkins_bdd_skipped'] or any(p.startswith('reports/behave/') for p in jk_xml):
            raise RuntimeError('Jenkins: übersprungene BDD-Stage fehlt.')
    return summary


def run(demo=False, case='green'):
    files = snapshot(SOURCE, demo, case)
    if not (STATE / 'project.json').exists():
        raise RuntimeError('Zuerst setup configure ausführen.')
    pid = load('project.json')['id']
    lint(pid, files)
    branch = ('demo' if demo else 'main') if case == 'green' else ('demo-' if demo else '') + case
    name = 'rabattshop-' + (branch if branch != 'main' else 'green')
    sha = commit_snapshot(pid, branch, files)
    print(f'{len(files)} Dateien als {branch}@{sha[:12]} übernommen. Lokale Dateien bleiben erhalten.')
    pipeline = wait_for('Warte auf die neue GitLab-Pipeline',
                        lambda: gl(f'/projects/{pid}/pipelines?sha={sha}&ref={branch}'), 120)[0]['id']
    number = start_jenkins(name, sha)
    print(f'GitLab:  {PUBLIC_GL}/root/rabattshop/-/pipelines/{pipeline}')
    print(f'Jenkins: {PUBLIC_JK}/job/{name}/{number}/')
    print('Beide Läufe verwenden Commit ' + sha)
    completed = {}

    def finished():
        gitlab = gl(f'/projects/{pid}/pipelines/{pipeline}')
        try:
            jenkins = jk(f'/job/{name}/{number}/api/json')
        except RuntimeError as exc:
            if 'HTTP 404' not in str(exc):
                raise
            return False
        states = (gitlab['status'], jenkins.get('result') or 'RUNNING')
        if completed.get('states') != states:
            print(f'GitLab: {states[0]} | Jenkins: {states[1]}')
            completed.update(states=states, gitlab=gitlab, jenkins=jenkins)
        return states[0] in ('success', 'failed', 'canceled', 'skipped') and states[1] != 'RUNNING'

    wait_for('Pipelines laufen', finished, 1200)
    expected = {'green': ('success', 'SUCCESS'), 'unit-red': ('failed', 'FAILURE'),
                'bdd-red': ('failed', 'FAILURE'), 'coverage-low': ('success', 'UNSTABLE')}[case]
    save(name + '-builds.json', {'sha': sha, 'branch': branch, 'pipeline': pipeline,
                               'jenkins_build': number, 'states': completed['states']})
    if completed['states'] != expected:
        raise RuntimeError(f'Erwartet {expected}, erhalten {completed["states"]}. Konsolenausgaben unter den obigen Build-Links öffnen.')
    collect(pid, pipeline, name, number, case, sha)
    print('CI-Prüfung abgeschlossen: Status und XML-Berichte entsprechen dem gewählten Fall.')


def credentials():
    print('Nur für diese lokale Schulungsinstanz:')
    print(PUBLIC_GL, 'Benutzer: root', 'Passwort:', secret('gitlab-password'))
    print(PUBLIC_JK, 'Benutzer: seminar', 'Passwort:', secret('jenkins-password'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('init', 'configure', 'run', 'credentials'))
    parser.add_argument('--demo', action='store_true', help='TODOs nur in der hochgeladenen Kopie ergänzen')
    parser.add_argument('--case', choices=('green', 'unit-red', 'bdd-red', 'coverage-low'), default='green')
    args = parser.parse_args()
    if args.action == 'run':
        run(args.demo, args.case)
    else:
        globals()[args.action]()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, FileNotFoundError) as exc:
        print('FEHLER:', exc, file=sys.stderr)
        sys.exit(1)
