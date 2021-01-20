import React from 'react';
import 'antd/dist/antd.css';
import { Router } from '@reach/router';
import './services/localization';

import { NotFound, PublicFrame, PrivateFrame, LoginPage, RegistrationPage, WelcomePage, SetupPage, ApiaryPage, ApiaryCreationPage, HivePage, HiveCreationPage, HiveDetailsPage } from './pages';
import { setupData, sections } from './constants';

class App extends React.Component {
  changeLanguage = ({ key }) => {
    window.changeLanguage(key);
    this.forceUpdate();
  }

  render () {
    return (
      <Router >
        <PrivateFrame path="/" languageCallback={this.changeLanguage}>
          <WelcomePage path="/" />
          <NotFound default />
        </PrivateFrame>

        <PrivateFrame path="/manage" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/manage/apiary" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_apiary} submenuItem={sections.submenu_apiary_list}>
          <ApiaryPage path="/"/>
        </PrivateFrame>

        <PrivateFrame path="/manage/apiary/create" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_apiary} submenuItem={sections.submenu_apiary_create}>
          <ApiaryCreationPage path="/" />
        </PrivateFrame>

        <PrivateFrame path="/manage/hive" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_list}>
          <HivePage path="/" />
        </PrivateFrame>

        <PrivateFrame path="/manage/hive/create" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_create}>
          <HiveCreationPage path="/" />
        </PrivateFrame>

        <PrivateFrame path="/manage/hive/:hiveId" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_hive} submenuItem={sections.submenu_hive_list}>
          <HiveDetailsPage path="/" />
        </PrivateFrame>

        <PrivateFrame path="/setup" languageCallback={this.changeLanguage} />

        <PrivateFrame path="/setup/apiary/honey_type" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_apiary} submenuItem={sections.submenu_setup_apiary_honey_type}>
          <SetupPage path="/" dataType={setupData.apiary_honey_type}/>
        </PrivateFrame>

        <PrivateFrame path="/setup/swarm/health" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_swarm} submenuItem={sections.submenu_setup_swarm_health}>
          <SetupPage path="/" dataType={setupData.swarm_health_status}/>
        </PrivateFrame>

        <PrivateFrame path="/setup/hive/beekeeper" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_hive} submenuItem={sections.submenu_setup_hive_beekeeper}>
          <SetupPage path="/" dataType={setupData.hive_beekeeper}/>
        </PrivateFrame>

        <PrivateFrame path="/setup/hive/condition" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_hive} submenuItem={sections.submenu_setup_hive_condition}>
          <SetupPage path="/" dataType={setupData.hive_condition}/>
        </PrivateFrame>

        <PrivateFrame path="/setup/event/type" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_event} submenuItem={sections.submenu_setup_event_type}>
          <SetupPage path="/" dataType={setupData.event_type}/>
        </PrivateFrame>

        <PrivateFrame path="/setup/event/status" languageCallback={this.changeLanguage} submenuTopic={sections.submenu_setup_event} submenuItem={sections.submenu_setup_event_status}>
          <SetupPage path="/" dataType={setupData.event_status}/>
        </PrivateFrame>

        <PrivateFrame path="/profil" languageCallback={this.changeLanguage}/>

        <PublicFrame path="/login" languageCallback={this.changeLanguage}>
          <LoginPage path="/" />
        </PublicFrame>

        <PublicFrame path="/register" languageCallback={this.changeLanguage}>
          <RegistrationPage path="/" />
        </PublicFrame>

      </Router>
    );
  }
}

export default App;
