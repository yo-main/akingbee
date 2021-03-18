import React from 'react';

import { Row } from 'antd';

import { activationRequest } from '../services/authentication';
import { LOADING_STATUS, getGenericPage, NOT_FOUND_STATUS } from './generic';

export class ActivationPage extends React.Component {
  state = {pageStatus: LOADING_STATUS, content: ""}

  async componentDidMount() {
    let userId = this.props.hiveId;
    let activationId = this.props.activationId;

    try {
      let response = await activationRequest({userId, activationId});
      console.log(response)
      let content = response.status === 200 ? window.i18n("sentence.accountAlreadyActivated") : window.i18n("sentence.accountJustActivated")
      this.setState({pageStatus: null, content: content})

    } catch (error) {
      this.setState((state) => {
        state["pageStatus"] = NOT_FOUND_STATUS;
        return state;
      })
    }
  }


  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    return (
      <Row justify="center" style={{ paddingTop: "150px"}}>
        <p>
          {this.state["content"]}
        </p>
      </Row>
    )
  }
}