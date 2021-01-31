import React from 'react';

import { EditorState } from 'draft-js';
import { Editor } from "react-draft-wysiwyg";
import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";

const TOOLBAR = {
  options: ['inline', 'blockType', 'fontSize', 'fontFamily', 'list', 'textAlign', 'colorPicker',],
  inline: {
    options: ['bold', 'italic', 'underline', 'strikethrough'],
  },
  blockType: {
    options: ['Normal', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Blockquote'],
  },
  colorPicker: {
    colors: [
      'rgb(97,189,109)', 'rgb(44,130,201)', 'rgb(147,101,184)', 'rgb(71,85,119)',
      'rgb(204,204,204)', 'rgb(0,0,0)', 'rgb(251,160,38)', 'rgb(226,80,65)',
    ]
  },
}


export function RichEditor(props) {

  const [editorState, setEditorState] = React.useState(EditorState.createEmpty());

  const onEditorStateChange = (editorState) => {
    setEditorState(editorState);
  };

  return (
    <Editor
      editorState={editorState}
      onChange={props.onChange}
      toolbarClassName="toolbarClassName"
      wrapperClassName="wrapperClassName"
      editorClassName="editorClassName"
      onEditorStateChange={onEditorStateChange}
      editorStyle={{height: '200px', border: '1px solid lightgrey'}}
      toolbar={TOOLBAR}
    />
  )
}