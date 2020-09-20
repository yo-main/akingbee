import React from 'react';
import 'antd/dist/antd.css';
import { Router } from '@reach/router';
import './services/localization';

import { PublicFrame, PrivateFrame, LoginPage, RegistrationPage, WelcomePage } from './pages';

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
        <PrivateFrame path="/manage" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/setup" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/profil" languageCallback={this.changeLanguage} />

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
