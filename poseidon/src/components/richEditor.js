import React from 'react';

import { Editor } from '@tinymce/tinymce-react';


export function RichEditor(props) {
  return (
    <>
      <Editor
        apiKey={process.env.REACT_APP_TINYCLOUD_API_KEY}
        onInit={(evt, editor) => props.editorRef.current = editor}
        initialValue={props.defaultContent}
        init={{
          height: 500,
          menubar: false,
          plugins: [
            'advlist autolink lists link image charmap print preview anchor',
            'searchreplace visualblocks code fullscreen',
            'insertdatetime media table paste code help wordcount'
          ],
          toolbar: 'undo redo | formatselect | ' +
          'bold italic backcolor forecolor | alignleft aligncenter ' +
          'alignright alignjustify | bullist numlist outdent indent | ' +
          'removeformat | help',
          content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
        }}
      />
    </>
  );
}

// deprecated (not working as intended)
export function EditorReadOnly(props) {
  const editorRef = React.useRef(null);
  return (
    <>
      <Editor
        apiKey={process.env.REACT_APP_TINYCLOUD_API_KEY}
        onInit={(evt, editor) => {
          editor.readonly = 1;
          editor.theme = "advanced";
          editorRef.current = editor;
        }}
        initialValue={props.content}
        readonly = {true}
      />
    </>
  );
}