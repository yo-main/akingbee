import React from 'react';

import { Button, Form, Row, Col, Cascader } from 'antd';
import { PlusOutlined, MinusCircleOutlined, CheckCircleOutlined } from '@ant-design/icons'

import { formItemLayoutWithoutLabel } from '../constants';

export const formItemLayoutOptional = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 8 },
  },
  wrapperCol: {
    xs: { span: 20 },
    sm: { span: 12 },
  },
};



export class OptionalFormItem extends React.Component {
  state = {
    active: false
  }

  setActive = () => {
    this.setState((state) => {
      state.active = true;
    })
    this.forceUpdate();
  }

  setInative = () => {
    this.setState((state) => {
      state.active = false;
    });
    this.forceUpdate();
  }

  render() {
    return (
      <>
        {this.state.active === false ?
          <Form.Item {...formItemLayoutWithoutLabel}>
            <Button
              type="dashed"
              onClick={this.setActive}
              icon={<PlusOutlined />}
            >
              {this.props.buttonName}
            </Button>
          </Form.Item>
          :
          <Row>
            <Col span='20'>
              <Form.Item {...this.props} style={{ paddingLeft: '10%' }}>
                {this.props.children}
              </Form.Item>
            </Col>
            <Col>
              <MinusCircleOutlined
                onClick={this.setInative}
                style={{ paddingTop: '70%', paddingLeft: '50%' }}
              />
            </Col>
          </Row>
        }
      </>
    )
  }
}



export function CascaderForm(props) {
  const [value, setValue] = React.useState([]);
  const [selected, setSelected] = React.useState(false);

  const onChange = (v) => {

    if (v) {
      setValue(v);

      if (v.length > 0 && !selected) {
          setSelected(true);
      } else if (v.length === 0 && selected) {
        setSelected(false);
      }
    }
  }

  const onFinish = (form) => {
    setValue([]);
    setSelected(false);
    props.onFinish(form);
  }

  let buttons;
  if (selected) {
    buttons = (
      <Form.Item>
        <Button htmlType='submit' icon={<CheckCircleOutlined />} type='text' />
      </Form.Item>
    )
  }

  return (
    <Form onFinish={(e) => onFinish(e)}>
      <Row>
        <Col>
          <Form.Item name="action">
            <Cascader value={value} options={props.options} onChange={(e) => onChange(e)} placeholder={props.title} />
          </Form.Item>
        </Col>
        <Col>
          {buttons}
        </Col>
      </Row>
    </Form>
  )
}
