import React from 'react';
import { Modal, Button} from 'antd';
import { PlusOutlined } from '@ant-design/icons'
import Base from 'antd/lib/typography/Base';

class BaseModal extends React.Component {
  state = { visible: false}

  showModal = () => {
    this.setState((state) => ({visible: true}))
  };

  closeModal = e => {
    this.setState((state) => ({visible: false}))
  };

  entrypoint() {
    return ""
  }

  getFooter() {
    return (
      this.props.formId ?
      [
        <Button type="primary" onClick={this.closeModal}>{window.i18n("word.cancel")}</Button>,
        <Button type="secondary" onClick={this.closeModal} form={this.props.formId} htmlType="submit">{window.i18n("word.submit")}</Button>,
      ]
      :
      [
        <Button type="primary" onClick={this.closeModal}>{window.i18n("word.cancel")}</Button>,
        <Button type="secondary" onClick={this.closeModal}>{window.i18n("word.submit")}</Button>,
      ]
    )
  }

  render() {
    return (
      <>
        {this.entrypoint()}
       <Modal
          title={this.props.title}
          visible={this.state.visible}
          onCancel={this.closeModal}
          onOk={this.closeModal}
          footer={this.getFooter()}
        >
          {this.props.children}
        </Modal>
      </>
    );
  }
}

export class FormButtonModal extends BaseModal {
  entrypoint() {
    return (
      <Button onClick={this.showModal}>
        {this.props.buttonContent}
      </Button>
    )
  }
}

export class FormLinkModal extends BaseModal {
  entrypoint() {
    return (
      <a onClick={this.showModal}>
        {this.props.linkContent}
      </a>
    )
  }
}
