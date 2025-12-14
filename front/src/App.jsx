import React, { useState } from 'react';
import WorkflowEditor from './components/WorkflowEditor';
import WorkflowList from './components/WorkflowList';

const App = () => {
  const [currentView, setCurrentView] = useState('editor'); // 'editor' or 'list'
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  return (
    <div className="min-h-screen starry-background">
      {/* Header */}
      <header className="bg-slate-800 shadow-lg relative z-10">
        <div className="px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">Dify-like Workflow Editor</h1>
          <nav>
            <button 
              onClick={() => setCurrentView('editor')}
              className={`mr-4 px-3 py-2 rounded-md ${currentView === 'editor' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-700'}`}
            >
              Editor
            </button>
            <button 
              onClick={() => setCurrentView('list')}
              className={`px-3 py-2 rounded-md ${currentView === 'list' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:bg-slate-700'}`}
            >
              Workflows
            </button>
          </nav>
        </div>
      </header>

      <main>
        <div className="py-6">
          {currentView === 'editor' ? (
            <WorkflowEditor workflow={selectedWorkflow} />
          ) : (
            <div className="relative z-0">
              <WorkflowList onSelectWorkflow={(workflow) => {
                setSelectedWorkflow(workflow);
                setCurrentView('editor');
              }} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;