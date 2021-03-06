import React, { useEffect, useState } from 'react';
import { updateValueOnNode } from "../functions/node";
import { isStringBoolean } from '../functions/utils';
import './styles.scss';

export default function InputNode({ nodeDatum, updateValue, tree, setTree, queue, setNewSocket, socket}: {nodeDatum:any, updateValue: Function, tree:any, setTree:React.Dispatch<any>, queue:any, setNewSocket:React.Dispatch<any>, socket:any}) {

  const [value, setValue] = useState(nodeDatum.value);
  const [checked, setChecked] = useState(nodeDatum.value);
  
  useEffect(()=> {
    if (nodeDatum.value !== undefined) {
      setValue(nodeDatum.value);
      setChecked(nodeDatum.value);
    }
  }, [nodeDatum.value]);

  function handleClick(e:any){
    if (nodeDatum.nature === "radio"){
      handleChange(e);
    }
  }

  function handleChange(e: any) {
    if (nodeDatum.nature === "checkbox") {
      setChecked(!!e.target.checked)
    } else {
      setValue(isStringBoolean(e.target.value) ? !(e.target.value === "true") : e.target.value);
    }
  }

  useEffect(() => {
    if (value !== nodeDatum.value) {
      const delayedUpdate = setTimeout(() => {
        if (nodeDatum.nature === "radio"){
          //@ts-ignore
          const associatedRadioInputs = document.querySelectorAll("input[type='radio'], input[class='" + nodeDatum.syntaxKey + "'], input[value='true']");
          associatedRadioInputs.forEach((input) =>{
            if (!input.classList.contains(nodeDatum.path + "_input")){
              updateValueOnNode(false, input.classList[0].split("_")[0], tree, setTree, queue, setNewSocket, socket);
            }
          })
        }
        updateValueOnNode(value, nodeDatum.path + "_input", tree, setTree, queue, setNewSocket, socket);
        updateValue(value)
      }, 400);
      return () => clearTimeout(delayedUpdate);
    }
  }, [value])

  useEffect(() => {
    if (checked !== nodeDatum.value) {
      const delayedUpdate = setTimeout(() => {
        updateValueOnNode(checked, nodeDatum.path + "_input", tree, setTree, queue, setNewSocket, socket);
        updateValue(checked)
      }, 400);
      return () => clearTimeout(delayedUpdate);
    }
  }, [checked])

  return (
      <g className={nodeDatum.path}>
        <foreignObject width={120} height={70} y={-35} x={-60}>
          <div className="node-div">
            <div className="node-content">
              <label>{nodeDatum.syntaxKey}</label>
              <input
                className={nodeDatum.path + "_input " + nodeDatum.syntaxKey}
                type={nodeDatum.nature}
                checked={checked}
                value={value}
                name={nodeDatum.syntaxKey}
                onChange={handleChange}
                onClick={handleClick}
              />
            </div>
          </div>
        </foreignObject>
      </g>
    )
}
