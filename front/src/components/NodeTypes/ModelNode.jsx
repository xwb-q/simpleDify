import React, { useState, useEffect } from 'react';
import { Handle, Position } from 'reactflow';

const ModelNode = ({ data, id, dragging }) => {
  const [inputValue, setInputValue] = useState(data.inputValue || '');
  const [outputValue, setOutputValue] = useState(data.outputValue || '');
  const [customPrompt, setCustomPrompt] = useState(data.prompt || '');

  // 当节点数据变化时更新状态
  useEffect(() => {
    setInputValue(data.inputValue || '');
    setOutputValue(data.outputValue || '');
    setCustomPrompt(data.prompt || '');
  }, [data.inputValue, data.outputValue, data.prompt]);

  // 格式化输出值用于显示
  const formatOutputValue = (value) => {
    if (typeof value === 'object' && value !== null) {
      // 如果是对象，尝试提取有用的信息
      if (value.choices && Array.isArray(value.choices) && value.choices.length > 0) {
        // 这看起来像是一个OpenAI API响应
        return value.choices[0].message?.content || JSON.stringify(value);
      }
      return JSON.stringify(value, null, 2);
    }
    return value || '';
  };

  const handlePromptChange = (e) => {
    const newPrompt = e.target.value;
    setCustomPrompt(newPrompt);
    // 更新节点数据
    if (data.onPromptChange) {
      data.onPromptChange(id, newPrompt);
    }
  };

  return (
    <div 
      className="px-4 py-2 shadow-md rounded-md bg-slate-800 border-2 border-blue-500 min-w-[200px]"
    >
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-blue-500"
      />
      <div className="flex items-center">
        <div className="ml-2">
          <span className="text-xs font-bold text-blue-400">MODEL</span>
          <div className="text-sm font-medium text-slate-200">{data.label}</div>
        </div>
      </div>
      <div className="mt-2">
        <label className="block text-xs text-slate-400 mb-1">Custom Prompt:</label>
        <textarea
          value={customPrompt}
          onChange={handlePromptChange}
          className="w-full px-2 py-1 text-xs bg-slate-700 text-slate-200 rounded border border-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500"
          rows="3"
          placeholder="Enter custom prompt..."
        />
      </div>
      <div className="mt-2">
        <label className="block text-xs text-slate-400 mb-1">Input:</label>
        <div className="w-full px-2 py-1 text-xs bg-slate-700 text-slate-200 rounded border border-slate-600 min-h-[40px]">
          {inputValue || 'Waiting for input...'}
        </div>
      </div>
      <div className="mt-2">
        <label className="block text-xs text-slate-400 mb-1">Output:</label>
        <div className="w-full px-2 py-1 text-xs bg-slate-700 text-slate-200 rounded border border-slate-600 min-h-[40px]">
          <pre className="whitespace-pre-wrap">{formatOutputValue(outputValue)}</pre>
        </div>
      </div>
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-blue-500"
      />
    </div>
  );
};

export default ModelNode;