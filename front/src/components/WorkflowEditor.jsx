import React, { useState, useRef, useCallback, useEffect, useMemo } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  MarkerType,
} from 'reactflow';
import 'reactflow/dist/style.css';
import StartNode from './NodeTypes/StartNode';
import ModelNode from './NodeTypes/ModelNode';
import EndNode from './NodeTypes/EndNode';
import { createWorkflow, updateWorkflow, executeWorkflow } from '../services/api';

const initialNodes = [
  {
    id: '1',
    type: 'startNode',
    position: { x: 250, y: 50 },
    data: { label: 'Start' },
    draggable: true,
  },
];

const initialEdges = [];

// Define nodeTypes at the module level
const nodeTypes = {
  startNode: StartNode,
  modelNode: ModelNode,
  endNode: EndNode,
};

const WorkflowEditor = ({ workflow }) => {
  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [workflowName, setWorkflowName] = useState(workflow?.name || '');
  const [workflowDescription, setWorkflowDescription] = useState(workflow?.description || '');
  const [executionResult, setExecutionResult] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [userInput, setUserInput] = useState('');

  // Delete selected node with keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Delete' && selectedNodeId) {
        setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
        setEdges((eds) => eds.filter((edge => edge.source !== selectedNodeId && edge.target !== selectedNodeId)));
        setSelectedNodeId(null);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [selectedNodeId, setNodes, setEdges]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({
      ...params,
      markerEnd: { type: MarkerType.ArrowClosed },
    }, eds)),
    [setEdges],
  );

  const onDragOver = useCallback((event) => {
    console.log('onDragOver called:', event.type, event.clientX, event.clientY);
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      console.log('onDrop called:', event.type, event.clientX, event.clientY);
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');
      console.log('Dropped type:', type);

      // Check if the dropped element is a valid node type
      if (!type || !nodeTypes[type]) {
        console.log('Invalid type or type not found in nodeTypes');
        return;
      }

      if (!reactFlowInstance) {
        console.log('ReactFlow instance not ready');
        return;
      }

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      console.log('ReactFlow bounds:', reactFlowBounds);
      
      // Get the position where the node was dropped
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });
      console.log('Calculated drop position:', position);

      // Create a new node
      const newNode = {
        id: `${+new Date()}`, // Use timestamp for unique ID
        type,
        position,
        data: { label: `${type.replace('Node', '')} Node` },
        draggable: true,
      };

      console.log('Adding new node:', newNode);
      setNodes((nds) => {
        const updatedNodes = nds.concat(newNode);
        console.log('Updated nodes array:', updatedNodes);
        return updatedNodes;
      });
    },
    [reactFlowInstance, setNodes],
  );

  // 处理Start节点输入变化
  const handleStartNodeInputChange = useCallback((nodeId, inputValue) => {
    setNodes(nds => 
      nds.map(node => {
        if (node.id === nodeId) {
          return {
            ...node,
            data: {
              ...node.data,
              inputValue: inputValue
            }
          };
        }
        return node;
      })
    );
  }, [setNodes]);

  // 处理Model节点提示变化
  const handleModelNodePromptChange = useCallback((nodeId, prompt) => {
    setNodes(nds => 
      nds.map(node => {
        if (node.id === nodeId) {
          return {
            ...node,
            data: {
              ...node.data,
              prompt: prompt
            }
          };
        }
        return node;
      })
    );
  }, [setNodes]);

  const onSave = async () => {
    try {
      // Encode nodes and edges data in the description as JSON
      const workflowMetadata = {
        nodes: nodes.map(node => ({
          id: node.id,
          type: node.type,
          position: node.position,
          data: node.data,
        })),
        edges: edges.map(edge => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
        })),
        description: workflowDescription, // Store the actual description in metadata
      };

      const workflowData = {
        name: workflowName || 'Untitled Workflow',
        description: JSON.stringify(workflowMetadata),
      };

      if (workflow && workflow.id) {
        // Update existing workflow
        await updateWorkflow(workflow.id, workflowData);
      } else {
        // Create new workflow
        await createWorkflow(workflowData);
      }

      alert('Workflow saved successfully!');
    } catch (error) {
      console.error('Failed to save workflow:', error);
      alert('Failed to save workflow');
    }
  };

  const onExecute = async () => {
    if (!workflow || !workflow.id) {
      alert('Please save the workflow first');
      return;
    }

    setIsExecuting(true);
    setExecutionResult(null);

    try {
      const response = await executeWorkflow(workflow.id, userInput || null);
      setExecutionResult(response.data);
      
      // 更新节点显示执行结果
      if (response.data.results && response.data.results.length > 0) {
        let updatedNodes = [...nodes];
        
        // 更新每个节点的输出显示
        response.data.results.forEach((result, index) => {
          if (result.result && result.result.success) {
            const nodeId = getNodeIdByTaskOrder(index, updatedNodes);
            if (nodeId) {
              updatedNodes = updatedNodes.map(node => {
                if (node.id === nodeId) {
                  return {
                    ...node,
                    data: {
                      ...node.data,
                      outputValue: result.result.data
                    }
                  };
                }
                return node;
              });
            }
          }
        });
        
        // 更新End节点的输出显示为最后一个节点的输出
        if (response.data.final_output) {
          updatedNodes = updatedNodes.map(node => {
            if (node.type === 'endNode') {
              return {
                ...node,
                data: {
                  ...node.data,
                  outputValue: response.data.final_output
                }
              };
            }
            return node;
          });
        }
        
        setNodes(updatedNodes);
      }
    } catch (error) {
      console.error('Failed to execute workflow:', error);
      setExecutionResult({ error: error.response?.data?.detail || 'Failed to execute workflow' });
    } finally {
      setIsExecuting(false);
    }
  };

  // 根据任务顺序获取节点ID
  const getNodeIdByTaskOrder = (order, nodesList) => {
    const modelNodes = nodesList.filter(node => node.type === 'modelNode');
    if (order < modelNodes.length) {
      return modelNodes[order].id;
    }
    return null;
  };

  const onNodeDoubleClick = useCallback((event, node) => {
    console.log('Node double clicked:', node);
    const nodeName = prompt('Enter node name:', node.data.label);
    if (nodeName !== null) {
      setNodes(nds =>
        nds.map(n => {
          if (n.id === node.id) {
            return {
              ...n,
              data: {
                ...n.data,
                label: nodeName,
              },
            };
          }
          return n;
        })
      );
    }
  }, [setNodes]);

  const onNodeClick = useCallback((event, node) => {
    console.log('Node clicked:', node);
    setSelectedNodeId(node.id);
  }, [setSelectedNodeId]);

  // Log when reactFlowInstance changes
  useEffect(() => {
    if (reactFlowInstance) {
      console.log('ReactFlow instance initialized:', reactFlowInstance);
    }
  }, [reactFlowInstance]);

  // Log nodes changes
  useEffect(() => {
    console.log('Nodes updated:', nodes);
  }, [nodes]);
  
  // 添加这个useEffect来检查DOM元素
  useEffect(() => {
    if (reactFlowWrapper.current) {
      console.log('ReactFlow wrapper element:', reactFlowWrapper.current);
    }
  }, []);

  // Initialize workflow data when workflow prop changes
  useEffect(() => {
    console.log('Initializing workflow data:', workflow);
    if (workflow && workflow.id) {
      // Set workflow metadata
      setWorkflowName(workflow.name || '');
      
      // Parse nodes and edges from the description field
      let workflowNodes = [...initialNodes];
      let workflowEdges = [...initialEdges];
      let description = '';
      
      if (workflow.description) {
        try {
          const metadata = JSON.parse(workflow.description);
          if (metadata.nodes && Array.isArray(metadata.nodes)) {
            workflowNodes = metadata.nodes.map(node => ({
              ...node,
              draggable: true,
              data: {
                ...node.data,
                onInputChange: handleStartNodeInputChange,
                onPromptChange: handleModelNodePromptChange
              }
            }));
          }
          if (metadata.edges && Array.isArray(metadata.edges)) {
            workflowEdges = metadata.edges;
          }
          // Extract the actual description from metadata
          description = metadata.description || '';
        } catch (e) {
          console.error('Failed to parse workflow metadata:', e);
          // If parsing fails, treat the whole description as text
          description = workflow.description || '';
        }
      }
      
      setWorkflowDescription(description);
      setNodes(workflowNodes);
      setEdges(workflowEdges);
    } else {
      // Reset to initial state when no workflow is provided
      setWorkflowName('');
      setWorkflowDescription('');
      setNodes(initialNodes.map(node => 
        node.type === 'startNode' 
          ? { ...node, data: { ...node.data, onInputChange: handleStartNodeInputChange } } 
          : node
      ));
      setEdges(initialEdges);
    }
  }, [workflow, setNodes, setEdges, handleStartNodeInputChange, handleModelNodePromptChange]);

  // 格式化执行结果用于显示
  const formatExecutionResult = (result) => {
    if (typeof result === 'object' && result !== null) {
      // 如果是对象，尝试提取有用的信息
      if (result.data) {
        // 这可能是来自模型服务的响应
        return result.data;
      }
      return JSON.stringify(result, null, 2);
    }
    return result || '';
  };

  return (
    <div className="h-[calc(100vh-200px)] flex flex-col relative">
      <div className="mb-4 flex justify-between items-center px-4">
        <div className="flex space-x-4">
          <input
            type="text"
            placeholder="Workflow Name"
            value={workflowName}
            onChange={(e) => {
              console.log('Workflow name changed:', e.target.value);
              setWorkflowName(e.target.value);
            }}
            className="px-3 py-2 border border-slate-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-slate-800 text-slate-200"
          />
          <input
            type="text"
            placeholder="Description"
            value={workflowDescription}
            onChange={(e) => {
              console.log('Workflow description changed:', e.target.value);
              setWorkflowDescription(e.target.value);
            }}
            className="px-3 py-2 border border-slate-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-slate-800 text-slate-200"
          />
        </div>
        <div className="space-x-2">
          <button
            onClick={(e) => {
              console.log('Save button clicked');
              onSave();
            }}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Save Workflow
          </button>
          {workflow && workflow.id && (
            <button
              onClick={(e) => {
                console.log('Execute button clicked');
                onExecute();
              }}
              disabled={isExecuting}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
            >
              {isExecuting ? 'Executing...' : 'Execute Workflow'}
            </button>
          )}
        </div>
      </div>

      {/* User input section for workflow execution */}
      {workflow && workflow.id && (
        <div className="mb-4 px-4">
          <div className="flex items-center space-x-2">
            <label className="text-slate-200">User Input:</label>
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Enter your prompt for this execution..."
              className="flex-1 px-3 py-2 border border-slate-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 bg-slate-800 text-slate-200"
            />
          </div>
        </div>
      )}

      {executionResult && (
        <div className="mb-4 p-4 bg-slate-800 rounded-md border border-slate-700 mx-4">
          <h3 className="text-lg font-medium text-slate-200">Execution Result</h3>
          <pre className="mt-2 text-sm text-slate-400 whitespace-pre-wrap">
            {formatExecutionResult(executionResult)}
          </pre>
        </div>
      )}

      <div className="flex-1 bg-slate-800 border border-slate-700 rounded-lg overflow-hidden mx-4">
        <div className="flex h-full relative">
          {/* Sidebar with node types */}
          <div className="w-48 bg-slate-800 border-r border-slate-700 p-4 relative z-10">
            <h3 className="font-medium text-slate-200 mb-2">Nodes</h3>
            <div 
              className="p-2 mb-2 bg-slate-700 border border-slate-600 rounded cursor-move text-slate-200 select-none"
              draggable
              onDragStart={(event) => {
                console.log('Model Node: Starting drag event');
                event.dataTransfer.setData('application/reactflow', 'modelNode');
                event.dataTransfer.effectAllowed = 'move';
                console.log('Model Node: Drag data set');
              }}
              onMouseDown={(e) => {
                console.log('Model Node: Mouse down event');
                e.stopPropagation();
              }}
              onTouchStart={(e) => {
                console.log('Model Node: Touch start event');
                e.stopPropagation();
              }}
            >
              Model Node
            </div>
            <div 
              className="p-2 mb-2 bg-slate-700 border border-slate-600 rounded cursor-move text-slate-200 select-none"
              draggable
              onDragStart={(event) => {
                console.log('End Node: Starting drag event');
                event.dataTransfer.setData('application/reactflow', 'endNode');
                event.dataTransfer.effectAllowed = 'move';
                console.log('End Node: Drag data set');
              }}
              onMouseDown={(e) => {
                console.log('End Node: Mouse down event');
                e.stopPropagation();
              }}
              onTouchStart={(e) => {
                console.log('End Node: Touch start event');
                e.stopPropagation();
              }}
            >
              End Node
            </div>
          </div>
          
          {/* Workflow editor area */}
          <div 
            ref={reactFlowWrapper} 
            className="flex-1 relative"
            onDrop={(event) => {
              console.log('Workflow area: Drop event received');
              onDrop(event);
            }}
            onDragOver={(event) => {
              console.log('Workflow area: Drag over event received');
              onDragOver(event);
            }}
            onClick={(e) => {
              console.log('Workflow editor area clicked');
            }}
            onMouseDown={(e) => {
              console.log('Workflow editor area mouse down');
            }}
          >
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={(changes) => {
                console.log('Nodes changed:', changes);
                // Check if there's a select change
                changes.forEach(change => {
                  if (change.type === 'select' && change.selected) {
                    setSelectedNodeId(change.id);
                  } else if (change.type === 'select' && !change.selected && selectedNodeId === change.id) {
                    setSelectedNodeId(null);
                  }
                });
                onNodesChange(changes);
              }}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onInit={(instance) => {
                console.log('ReactFlow onInit called');
                setReactFlowInstance(instance);
              }}
              onNodeDoubleClick={onNodeDoubleClick}
              onNodeClick={onNodeClick}
              nodeTypes={nodeTypes}
              fitView
              proOptions={{ hideAttribution: true }}
              // 添加这些属性以确保交互正常工作
              nodesDraggable={true}
              nodesConnectable={true}
              elementsSelectable={true}
            >
              <Controls style={{ color: '#e2e8f0' }} />
              <MiniMap style={{ backgroundColor: '#0f172a' }} />
              <Background variant="dots" gap={12} size={1} color="#334155" />
            </ReactFlow>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkflowEditor;