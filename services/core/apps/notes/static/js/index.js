const editor = new EditorJS({
    holder: 'editorjs',
    /** 
     * Available Tools list. 
     * Pass Tool's class or Settings object for each Tool you want to use 
     */
    tools:{
      header: {
        class: Header,
        inlineToolbar : true
      },
      delimiter: {
        class: Delimiter,
        inlineToolbar: true,
      },
      paragraph: {
       class: Paragraph,
       inlineToolbar: true,
       config: {
         placeholder: 'Write text, copy images, YouTube link, ...'
       }
      },
      embed: {
        class: Embed,
        inlineToolbar: true,
      },
      image: {
        class: SimpleImage,
        inlineToolbar: true,
        config: {
          placeholder: 'Paste image URL'
        }
      },
      list: {
        class: List,
        inlineToolbar: true,
        config: {
          defaultStyle: 'unordered'
        }
      },
      code: {
        class: CodeTool,
      },
      table: {
        class: Table,
        inlineToolbar: true,
      },
      Marker: {
        class: Marker,
        shortcut: 'CMD+SHIFT+M',
      },
      inlineCode: {
        class: InlineCode,
        shortcut: 'CMD+SHIFT+P',
      },
      checklist: {
        class: Checklist,
        inlineToolbar: true,
      },
  }
});

editor.isReady.then(() => {
  console.log('EditorJS is ready to work!')
  GetBlocks()
})


//function to call when pressing Save button
function SaveBlocks(){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          console.log(xhr.responseText);
        } else {
          alert("There was a problem with the request.");
        }
      } else {
        console.log("Request not ready yet.")
      }
    };
    //Post request on "/editorjs_posting/" URL, connected to a view that parse the request and create blocks in the database (if they don't already exists)
    xhr.open("POST", "/notes/editorjs_posting/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    editor.save().then((data) => {
      console.log(data);
      xhr.send(JSON.stringify(data));
      console.log(xhr)
    })
};

//function to call on page loading
function GetBlocks(){
  var xhr = new XMLHttpRequest(); 
  xhr.onreadystatechange = function(){
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        console.log(xhr.responseText);
        editor.render(JSON.parse(xhr.responseText))
      } else {
        alert("There was a problem with the request.");
      }
    } else {
      console.log("Request not ready yet.")
  }
  }
  //Get request on the "/editorjs_getting/" URL, which is connected to a view that return all blocks in the editorJS format
  xhr.open("GET", "/notes/editorjs_getting/", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send()
}
