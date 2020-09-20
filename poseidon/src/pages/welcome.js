import React from 'react';
import { Redirect } from '@reach/router';

export function WelcomePage(props) {
  return <Redirect from="/" to="manage" noThrow />
}