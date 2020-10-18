import React from 'react';
import { Form, Input } from 'antd';

import { notificate } from '../lib/common';

function onFailed(err) {
  notificate("error", "Failed")
}

export function AddNewData(props) {
  return (
    <Form id="addNewDataFormId" name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label="New entry" name="newEntry"
        rules={[{ required: true}]}
      >
        <Input />
      </Form.Item>
      <Form.Item name="dataType" initialValue={props.dataType} hidden={true}/>
    </Form>
  )
}