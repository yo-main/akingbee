import React from 'react';
import { Modal, Button } from 'antd';

class BaseModal extends React.Component {

  showModal = () => {
    this.setState((state) => ({ visible: true }))
  };

  closeModal = e => {
    this.setState((state) => ({ visible: false }))
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
          bodyStyle={this.props.modalStyle}
        >
          {this.props.children}
        </Modal>
      </>
    );
  }
}

export class FormButtonModal extends BaseModal {
  state = { visible: false }

  entrypoint() {
    return (
      <Button icon={this.props.buttonIcon} type="default" shape="square" onClick={this.showModal} />
    )
  }
}

export class FormLinkModal extends BaseModal {
  state = { visible: false }

  entrypoint() {
    return (
      <Button onClick={this.showModal} type="link" disabled={this.props.disabled}>
        {this.props.linkContent}
      </Button>
    )
  }
}

export class FormModal extends BaseModal {
  showModal = () => {
    this.props.activate()
  };

  closeModal = e => {
    this.props.deactivate()
  };

  getFooter = () => {
    return (
      <>
        <Button type="primary" onClick={this.closeModal}>{window.i18n("word.cancel")}</Button>,
        <Button type="secondary" onClick={this.closeModal} form={this.props.formId} htmlType="submit">{window.i18n("word.submit")}</Button>,
      </>
    )
  };

  render() {
    return (
      <>
        <Modal
          title={this.props.title}
          visible={this.props.visible}
          onCancel={this.closeModal}
          onOk={this.closeModal}
          footer={this.getFooter()}
          bodyStyle={this.props.modalStyle}
        >
          {this.props.children}
        </Modal>
      </>
    );
  }
}
