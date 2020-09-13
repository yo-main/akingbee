import React from 'react';
import 'antd/dist/antd.css';
import { Router } from '@reach/router';
import './services/localization';

import { PublicFrame, PrivateFrame, LoginPage } from './pages';

class App extends React.Component {
  changeLanguage = ({ key }) => {
    window.changeLanguage(key);
    this.forceUpdate();
  }

  render () {
    return (
      <Router >
        <PrivateFrame path="/" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/manage" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/setup" languageCallback={this.changeLanguage} />
        <PrivateFrame path="/profil" languageCallback={this.changeLanguage} />

        <PublicFrame path="/login" languageCallback={this.changeLanguage}>
          <LoginPage path="/" />
        </PublicFrame>
      </Router>
    );
  }
}

export default App;
