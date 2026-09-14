import jenkins.model.Jenkins
import hudson.model.User
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import jenkins.install.InstallState
import jenkins.model.JenkinsLocationConfiguration

def instance = Jenkins.get()
def realm = instance.securityRealm
if (!(realm instanceof HudsonPrivateSecurityRealm)) {
    realm = new HudsonPrivateSecurityRealm(false)
    instance.setSecurityRealm(realm)
}
if (User.getById('seminar', false) == null) {
    realm.createAccount('seminar', new File('/state/jenkins-password').text.trim())
}
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)
instance.setNumExecutors(1)
JenkinsLocationConfiguration.get().setUrl(System.getenv('SEMINAR_JENKINS_URL'))
instance.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
instance.save()
