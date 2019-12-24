function nodeScriptReplace(node) {
        if ( nodeScriptIs(node) === true ) {
                node.parentNode.replaceChild( nodeScriptClone(node) , node );
        }
        else {
                var i        = 0;
                var children = node.childNodes;
                while ( i < children.length ) {
                        nodeScriptReplace( children[i++] );
                }
        }

        return node;
}
function nodeScriptIs(node) {
        return node.tagName === 'SCRIPT';
}
function nodeScriptClone(node){
        var script  = document.createElement("script");
        script.text = node.innerHTML;
        for( var i = node.attributes.length-1; i >= 0; i-- ) {
                script.setAttribute( node.attributes[i].name, node.attributes[i].value );
        }
        return script;
}

export {nodeScriptReplace};
