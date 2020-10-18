import React from 'react';
import { Modal as AntdModal, Button} from 'antd';

export class Modal extends React.Component {

  render() {
    const footer = (
      this.props.formId ?
      [
        <Button type="primary" onClick={this.props.closeModal}>{window.i18n("word.cancel")}</Button>,
        <Button type="secondary" onClick={this.props.closeModal} form={this.props.formId} htmlType="submit">{window.i18n("word.submit")}</Button>,
      ]
      :
      [
        <Button type="primary" onClick={this.props.closeModal}>{window.i18n("word.cancel")}</Button>,
        <Button type="secondary" onClick={this.props.closeModal}>{window.i18n("word.submit")}</Button>,
      ]
    )

    return (
      <AntdModal
        title={this.props.title}
        visible={this.props.visible}
        onCancel={this.props.closeModal}
        onOk={this.props.closeModal}
        footer={footer}
      >
        {this.props.children}
      </AntdModal>
    );
  }
}

