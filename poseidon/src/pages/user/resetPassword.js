import React from 'react';

import { Form, Input, Button, Row } from 'antd';
import { resetPasswordRequest, resetPassword, validateResetId } from '../../services/authentication';
import { LOADING_STATUS, getGenericPage, NOT_FOUND_STATUS } from '../generic';
import { dealWithError, notificate } from '../../lib/common';
import { ResetPasswordForm } from '../../forms/users';

export function RequestPasswordResetPage(props) {
  let onSubmit = async({username}) => {
    try {
      await resetPasswordRequest({username})
    } catch (error) {}  // we don't want to show any particular error here

    notificate('success', window.i18n('sentence.processResetPassword'))
  }

  return (
    <Row justify="center" style={{ paddingTop: '150px'}}>
      <Form labelCol={{span: 8}} onFinish={onSubmit} requiredMark={false}>
        <Form.Item label={window.i18n('word.username')} name="username" rules={[{ required: true, message: window.i18n('form.insertUsernameMessage')}]}>
          <Input />
        </Form.Item>
        <Form.Item wrapperCol={{offset: 8}}>
          <Button type="primary" htmlType="submit">
            {window.i18n('confirm.resetPassword')}
          </Button>
        </Form.Item>
      </Form>
    </Row>
  )
}

export class PasswordResetPage extends React.Component {
  state = {pageStatus: LOADING_STATUS}

  async componentDidMount() {

    let {userId, resetId} = this.props.match.params;

    try {
      await validateResetId({userId, resetId})
      this.setState((state) => {
        state["pageStatus"] = null;
        return state;
      })
    } catch (error) {
      this.setState((state) => {
        state["pageStatus"] = NOT_FOUND_STATUS;
        return state;
      })
    }
  }

  async onFinish(form) {
    try {
      await resetPassword(form);
      notificate("success", window.i18n("success.passwordReseted"));
      this.props.history.push("/login");
    } catch (error) {
      dealWithError(error);
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    return (
      <Row justify="center" style={{ paddingTop: '150px'}}>
        <ResetPasswordForm userId={this.props.userId} resetId={this.props.resetId} onFinish={this.onFinish} />
      </Row>
    )
  }
}

