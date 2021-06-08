import React from 'react';
import { Redirect } from 'react-router-dom';

export function WelcomePage(props) {
  return <Redirect from="/" to="manage" noThrow />
}