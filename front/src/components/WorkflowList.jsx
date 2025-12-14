import React, { useState, useEffect } from 'react';
import { getWorkflows, deleteWorkflow, getWorkflow } from '../services/api';

const WorkflowList = ({ onSelectWorkflow }) => {
  const [workflows, setWorkflows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWorkflows();
  }, []);

  const fetchWorkflows = async () => {
    try {
      const response = await getWorkflows();
      setWorkflows(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch workflows:', error);
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteWorkflow(id);
      fetchWorkflows();
    } catch (error) {
      console.error('Failed to delete workflow:', error);
    }
  };

  const handleEdit = async (workflow) => {
    try {
      // Fetch the complete workflow data from the backend
      const response = await getWorkflow(workflow.id);
      onSelectWorkflow(response.data);
    } catch (error) {
      console.error('Failed to fetch workflow details:', error);
      // Fallback to using the partial workflow data
      onSelectWorkflow(workflow);
    }
  };

  // Format the date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (loading) {
    return <div className="text-slate-300">Loading workflows...</div>;
  }

  return (
    <div className="bg-slate-800 shadow overflow-hidden sm:rounded-md border border-slate-700">
      <ul className="divide-y divide-slate-700">
        {workflows.map((workflow) => (
          <li key={workflow.id}>
            <div className="px-4 py-4 flex items-center justify-between sm:px-6">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-medium text-slate-200 truncate">
                  {workflow.name || `Workflow ${workflow.id}`}
                </h3>
                <p className="mt-1 text-sm text-slate-400 truncate">
                  Last updated: {formatDate(workflow.updated_at)}
                </p>
              </div>
              <div className="ml-4 flex-shrink-0 flex space-x-2">
                <button
                  onClick={() => handleEdit(workflow)}
                  className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(workflow.id)}
                  className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Delete
                </button>
              </div>
            </div>
          </li>
        ))}
        {workflows.length === 0 && (
          <li className="px-4 py-4 sm:px-6">
            <div className="text-center">
              <h3 className="text-lg font-medium text-slate-200">No workflows</h3>
              <p className="mt-1 text-sm text-slate-400">
                Get started by creating a new workflow.
              </p>
              <button
                onClick={() => onSelectWorkflow(null)}
                className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Create Workflow
              </button>
            </div>
          </li>
        )}
      </ul>
    </div>
  );
};

export default WorkflowList;