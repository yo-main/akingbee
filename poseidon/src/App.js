import React from 'react';
import 'antd/dist/antd.css';
import { Router } from '@reach/router';
import './services/localization';

import { PublicFrame, PrivateFrame, LoginPage, RegistrationPage, WelcomePage, SetupPage, ApiaryPage, ApiaryCreationPage, HivePage, HiveCreationPage } from './pages';
import { setupData } from './constants';

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
        </PrivateFrame>
        <PrivateFrame path="/manage" languageCallback={this.changeLanguage}>
          <ApiaryPage path="/apiary" />
          <ApiaryCreationPage path="/apiary/create" />
          <HivePage path="/hive" />
          <HiveCreationPage path="/hive/create" />
        </PrivateFrame>
        <PrivateFrame path="/setup" languageCallback={this.changeLanguage}>
          <SetupPage path="/swarm/health" dataType={setupData.swarm_health_status}/>
          <SetupPage path="/hive/beekeeper" dataType={setupData.hive_beekeeper}/>
          <SetupPage path="/hive/condition" dataType={setupData.hive_condition}/>
          <SetupPage path="/apiary/honey_type" dataType={setupData.apiary_honey_type}/>
          <SetupPage path="/event/type" dataType={setupData.event_type}/>
          <SetupPage path="/event/status" dataType={setupData.event_status}/>
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
