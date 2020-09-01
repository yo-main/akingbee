import Frame from '../../components/layout';
import { getLanguagePaths, getBasicProps } from '../../lib/common';
import { Form, Input, Button, Row } from 'antd';


class LoginPage extends Frame {

  onFinish(username, password) {
    console.log("success", username, password);
  }

  onFinishFailed() {
    console.log("failed");
  }

  getContent() {
    const locales = this.props.locales;
    return (
      <Row justify="center" style={{ paddingTop: "150px"}}>
        <Form labelCol={{span: 10}} onFinish={this.onFinish} onFinishFailed={this.onFinishFailed}>
          <Form.Item label={locales.Username} name="username" rules={[{ required: true, message: locales.InsertUsernameMessage}]}>
            <Input />
          </Form.Item>
          <Form.Item label={locales.Password} name="password" rules={[{ required: true, message: locales.InsertPasswordMessage}]}>
            <Input.Password />
          </Form.Item>
          <Form.Item wrapperCol={{offset: 10, span: 3}}>
            <Button type="primary" htmlType="submit">
              {this.props.locales.LoginSubmit}
            </Button>
          </Form.Item>
        </Form>
      </Row>
    )
  }
}


export default function Home({ locales, lang }) {
  return <LoginPage locales={locales} lang={lang} hideMenu={true} />;
}

export async function getStaticProps({ params }) {
  let props = getBasicProps(params);
  return props;
}

export async function getStaticPaths() {
  const paths = getLanguagePaths();
  return {
    paths,
    fallback: false,
  };
}
