"use client";

import React, { useState, useEffect } from 'react';
import { 
  Terminal, 
  Cpu, 
  GitBranch, 
  Play, 
  Activity, 
  Shield, 
  Database, 
  Code, 
  Layers,
  CheckCircle2,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Dashboard() {
  const [logs, setLogs] = useState<string[]>([
    "Initializing Aether OS Core...",
    "Connecting to Multi-Agent Orchestrator...",
    "Sandbox Execution Engine: READY",
    "Vector Memory System: ONLINE",
  ]);

  const [agents, setAgents] = useState([
    { name: "Product Manager", status: "idle", icon: <Layers className="w-5 h-5" /> },
    { name: "Tech Lead", status: "active", icon: <Cpu className="w-5 h-5" /> },
    { name: "Backend Engineer", status: "idle", icon: <Code className="w-5 h-5" /> },
    { name: "QA Engineer", status: "idle", icon: <CheckCircle2 className="w-5 h-5" /> },
    { name: "DevOps Agent", status: "idle", icon: <Shield className="w-5 h-5" /> },
  ]);

  const [activeTask, setActiveTask] = useState("Architecting Microservices");

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws/execution/default');
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'status') {
        setLogs(prev => [...prev, data.data]);
      }
      if (data.type === 'agent_update') {
        setAgents(prev => prev.map(a => 
          a.name === data.agent ? { ...a, status: data.status } : a
        ));
      }
    };

    return () => socket.close();
  }, []);

  return (
    <div className="min-h-screen bg-[#050505] text-white p-6 font-sans">
      {/* Header */}
      <header className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-[#00f2ff] to-[#7000ff] rounded-lg flex items-center justify-center glow-primary">
            <Activity className="text-white w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold tracking-tighter">AETHER OS</h1>
        </div>
        <div className="flex items-center gap-4 bg-[#0f0f0f] border border-white/10 px-4 py-2 rounded-full">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm font-medium text-white/60">System Online</span>
          </div>
          <div className="w-[1px] h-4 bg-white/10" />
          <span className="text-sm font-mono text-[#00f2ff]">v1.0.0-alpha</span>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
        {/* Left Sidebar - Agents */}
        <div className="col-span-3 flex flex-col gap-6">
          <div className="glass p-6 flex-1">
            <h2 className="text-xs font-bold text-white/40 uppercase tracking-widest mb-6">Agent Swarm</h2>
            <div className="space-y-4">
              {agents.map((agent) => (
                <div key={agent.name} className={`flex items-center justify-between p-3 rounded-lg border transition-all ${agent.status === 'active' ? 'border-[#00f2ff]/50 bg-[#00f2ff]/5' : 'border-white/5 bg-white/2'}`}>
                  <div className="flex items-center gap-3">
                    <div className={`${agent.status === 'active' ? 'text-[#00f2ff]' : 'text-white/40'}`}>
                      {agent.icon}
                    </div>
                    <span className={`text-sm font-medium ${agent.status === 'active' ? 'text-white' : 'text-white/60'}`}>{agent.name}</span>
                  </div>
                  {agent.status === 'active' && <Loader2 className="w-4 h-4 text-[#00f2ff] animate-spin" />}
                </div>
              ))}
            </div>
          </div>

          <div className="glass p-6 h-48">
            <h2 className="text-xs font-bold text-white/40 uppercase tracking-widest mb-4">Memory Index</h2>
            <div className="flex items-center gap-3 text-white/60">
              <Database className="w-5 h-5" />
              <span className="text-sm">1,240 Vectors Indexed</span>
            </div>
          </div>
        </div>

        {/* Center - Execution Canvas */}
        <div className="col-span-6 flex flex-col gap-6">
          <div className="glass flex-1 relative overflow-hidden flex flex-center items-center justify-center">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[#00f2ff]/5 via-transparent to-transparent pointer-events-none" />
            
            {/* Visualizing LangGraph state (Mockup) */}
            <div className="flex flex-col items-center gap-8 z-10">
              <motion.div 
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 4, repeat: Infinity }}
                className="w-32 h-32 rounded-full border-2 border-[#00f2ff]/30 flex items-center justify-center bg-[#00f2ff]/10 glow-primary"
              >
                <Cpu className="w-12 h-12 text-[#00f2ff]" />
              </motion.div>
              <div className="text-center">
                <h3 className="text-lg font-bold mb-1">{activeTask}</h3>
                <p className="text-white/40 text-sm">Reasoning Loop #14 • Confidence: 98%</p>
              </div>
            </div>
          </div>

          {/* Terminal */}
          <div className="glass h-64 p-4 font-mono text-sm overflow-hidden flex flex-col">
            <div className="flex items-center justify-between mb-4 px-2">
              <div className="flex items-center gap-2">
                <Terminal className="w-4 h-4 text-[#00f2ff]" />
                <span className="text-xs font-bold text-white/40 uppercase tracking-widest">Execution Logs</span>
              </div>
              <div className="flex gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500/50" />
                <div className="w-2 h-2 rounded-full bg-yellow-500/50" />
                <div className="w-2 h-2 rounded-full bg-green-500/50" />
              </div>
            </div>
            <div className="flex-1 overflow-y-auto terminal-scroll px-2 space-y-1">
              {logs.map((log, i) => (
                <div key={i} className="flex gap-3">
                  <span className="text-white/20">[{new Date().toLocaleTimeString()}]</span>
                  <span className="text-white/80">{log}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Sidebar - Repository & Stats */}
        <div className="col-span-3 flex flex-col gap-6">
          <div className="glass p-6">
            <h2 className="text-xs font-bold text-white/40 uppercase tracking-widest mb-6">Repository Insight</h2>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <GitBranch className="w-5 h-5 text-[#7000ff]" />
                <div>
                  <div className="text-sm font-medium">main-dev-alpha</div>
                  <div className="text-xs text-white/40">34 commits • 12 files changed</div>
                </div>
              </div>
              <div className="p-3 bg-white/5 rounded border border-white/5">
                <div className="text-xs text-white/40 mb-2">Active PR</div>
                <div className="text-sm font-medium text-[#00f2ff]">#12 feat: autonomous-debugging</div>
              </div>
            </div>
          </div>

          <div className="glass p-6 flex-1">
            <h2 className="text-xs font-bold text-white/40 uppercase tracking-widest mb-6">Performance</h2>
            <div className="space-y-6">
              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-white/40">Token Efficiency</span>
                  <span className="text-[#00f2ff]">92%</span>
                </div>
                <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                  <div className="bg-[#00f2ff] h-full w-[92%]" />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-2">
                  <span className="text-white/40">Success Rate</span>
                  <span className="text-[#7000ff]">98.4%</span>
                </div>
                <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                  <div className="bg-[#7000ff] h-full w-[98%]" />
                </div>
              </div>
            </div>
          </div>

          <button 
            onClick={async () => {
              setLogs(prev => [...prev, "Starting Autonomous Mode..."]);
              try {
                await fetch('http://localhost:8000/projects', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    name: "Autonomous Project",
                    description: "Building a new microservice",
                  })
                });
              } catch (e) {
                console.error(e);
              }
            }}
            className="bg-gradient-to-r from-[#00f2ff] to-[#7000ff] hover:opacity-90 transition-all p-4 rounded-xl font-bold flex items-center justify-center gap-3 glow-primary w-full"
          >
            <Play className="w-5 h-5 fill-current" />
            START AUTONOMOUS MODE
          </button>
        </div>
      </div>
    </div>
  );
}
