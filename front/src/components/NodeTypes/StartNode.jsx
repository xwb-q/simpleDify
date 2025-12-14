import React, { useState, useEffect } from 'react';
import { Handle, Position } from 'reactflow';

const StartNode = ({ data, id, dragging }) => {
  const [inputValue, setInputValue] = useState(data.inputValue || '');

  // 当节点数据变化时更新状态
  useEffect(() => {
    setInputValue(data.inputValue || '');
  }, [data.inputValue]);

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    setInputValue(newValue);
    // 更新节点数据
    if (data.onInputChange) {
      data.onInputChange(id, newValue);
    }
  };

  return (
    <div 
      className="px-4 py-2 shadow-md rounded-md bg-slate-800 border-2 border-green-500 min-w-[200px]"
    >
      <div className="flex items-center">
        <div className="ml-2">
          <span className="text-xs font-bold text-green-400">START</span>
          <div className="text-sm font-medium text-slate-200">{data.label}</div>
        </div>
      </div>
      <div className="mt-2">
        <label className="block text-xs text-slate-400 mb-1">Input:</label>
        <textarea
          value={inputValue}
          onChange={handleInputChange}
          className="w-full px-2 py-1 text-xs bg-slate-700 text-slate-200 rounded border border-slate-600 focus:outline-none focus:ring-1 focus:ring-green-500"
          rows="3"
          placeholder="Enter input data..."
        />
      </div>
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-green-500"
      />
    </div>
  );
};

export default StartNode;