import React from 'react';
import { isLogged } from '../lib/auth';
import { getFullUrl } from '../lib/common';


export class Body extends React.Component {
  constructor(props) {
    super(props);
    this.state = {logged: null};
  }

  componentDidMount() {
    this.setState({logged: isLogged()});
  }

  render() {
    return <div>Hello</div>;
  }
}
