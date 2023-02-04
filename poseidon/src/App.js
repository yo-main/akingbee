import React from 'react';
import 'antd/dist/antd.css';
import { BrowserRouter, Switch, withRouter } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import './services/localization';

import { NotFound, PublicFrame, PrivateFrame, LoginPage, RegistrationPage, ProfilePage, WelcomePage, SetupPage, ApiaryPage, ApiaryCreationPage, HivePage, HiveCreationPage, HiveDetailsPage, ActivationPage, RequestPasswordResetPage, PasswordResetPage, AdminPage } from './pages';
import { setupData, sections } from './constants';

class App extends React.Component {
  changeLanguage = ({ key }) => {
    window.changeLanguage(key);
    this.forceUpdate();
  }

  render () {
    const ApiaryPageWithRouter = withRouter(ApiaryPage);
    const ApiaryCreationPageWithRouter = withRouter(ApiaryCreationPage);
    const HivePageWithRouter = withRouter(HivePage);
    const HiveCreationPageWithRouter = withRouter(HiveCreationPage);
    const HiveDetailsPageWithRouter = withRouter(HiveDetailsPage);
    const ActivationPageWithRouter = withRouter(ActivationPage);
    const RegistrationPageWithRouter = withRouter(RegistrationPage);
    const PasswordResetPageWithRouter = withRouter(PasswordResetPage);

    return (
      <ConfigProvider locale={window.locale}>
        <BrowserRouter >
          <Switch>
            <PublicFrame exact path="/" languageCallback={this.changeLanguage}>
              <WelcomePage />
            </PublicFrame>

            <PrivateFrame exact path="/manage" languageCallback={this.changeLanguage} />

            <PrivateFrame exact path="/manage/apiary" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_apiary} submenuItem={sections.submenu_apiary_list}>
              <ApiaryPageWithRouter />
            </PrivateFrame>

            <PrivateFrame exact path="/manage/apiary/create" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_apiary} submenuItem={sections.submenu_apiary_create}>
              <ApiaryCreationPageWithRouter />
            </PrivateFrame>

            <PrivateFrame exact path="/manage/hive" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_list}>
              <HivePageWithRouter />
            </PrivateFrame>

            <PrivateFrame exact path="/manage/hive/create" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_create}>
              <HiveCreationPageWithRouter />
            </PrivateFrame>

            <PrivateFrame exact path="/manage/hive/:hiveId" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_list}>
              <HiveDetailsPageWithRouter />
            </PrivateFrame>

            <PrivateFrame exact path="/setup" languageCallback={this.changeLanguage} />

            <PrivateFrame exact path="/setup/apiary/honey_kind" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_apiary} submenuItem={sections.submenu_setup_apiary_honey_kind} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.apiary_honey_kind} key={setupData.apiary_honey_kind} />
            </PrivateFrame>

            <PrivateFrame exact path="/setup/swarm/health" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_swarm} submenuItem={sections.submenu_setup_swarm_health} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.swarm_health_status} key={setupData.swarm_health_status} />
            </PrivateFrame>

            <PrivateFrame exact path="/setup/hive/beekeeper" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_hive} submenuItem={sections.submenu_setup_hive_beekeeper} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.hive_beekeeper} key={setupData.hive_beekeeper} />
            </PrivateFrame>

            <PrivateFrame exact path="/setup/hive/condition" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_hive} submenuItem={sections.submenu_setup_hive_condition} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.hive_condition} key={setupData.hive_condition} />
            </PrivateFrame>

            <PrivateFrame exact path="/setup/event/type" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_event} submenuItem={sections.submenu_setup_event_type} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.event_type} key={setupData.event_type} />
            </PrivateFrame>

            <PrivateFrame exact path="/setup/event/status" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_event} submenuItem={sections.submenu_setup_event_status} childUpdate={this.updateChild}>
              <SetupPage dataType={setupData.event_status} key={setupData.event_status} />
            </PrivateFrame>

            <PrivateFrame exact path="/profil" languageCallback={this.changeLanguage}>
              <ProfilePage />
            </PrivateFrame>

            <PrivateFrame exact path="/admin" languageCallback={this.changeLanguage}>
              <AdminPage />
            </PrivateFrame>

            <PublicFrame exact path="/login" languageCallback={this.changeLanguage}>
              <LoginPage />
            </PublicFrame>

            <PublicFrame exact path="/register" languageCallback={this.changeLanguage}>
              <RegistrationPageWithRouter />
            </PublicFrame>

            <PublicFrame exact path="/activate/:userId/:activationId" languageCallback={this.changeLanguage}>
              <ActivationPageWithRouter />
            </PublicFrame>

            <PublicFrame exact path="/password-reset" languageCallback={this.changeLanguage}>
              <RequestPasswordResetPage />
            </PublicFrame>

            <PublicFrame path="/password-reset/:userId/:resetId" languageCallback={this.changeLanguage}>
              <PasswordResetPageWithRouter />
            </PublicFrame>

            <PublicFrame path="*">
              <NotFound default />
            </PublicFrame>

          </Switch>
        </BrowserRouter>
      </ConfigProvider>
    );
  }
}

export default App;
