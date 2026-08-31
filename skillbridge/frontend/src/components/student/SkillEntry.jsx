import React, { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

const SkillEntry = ({ onSave }) => {
  const [skills, setSkills] = useState([])
  const [projects, setProjects] = useState([])
  const [skillInput, setSkillInput] = useState('')
  const [skillCategory, setSkillCategory] = useState('technical')
  const [skillProficiency, setSkillProficiency] = useState(50)

  const [projectName, setProjectName] = useState('')
  const [projectDescription, setProjectDescription] = useState('')
  const [projectTechnologies, setProjectTechnologies] = useState('')

  const addSkill = () => {
    if (skillInput.trim()) {
      setSkills([
        ...skills,
        {
          skill_name: skillInput.trim(),
          skill_category: skillCategory,
          proficiency: skillProficiency
        }
      ])
      setSkillInput('')
      setSkillProficiency(50)
      toast.success('Skill added')
    }
  }

  const removeSkill = (index) => {
    setSkills(skills.filter((_, i) => i !== index))
  }

  const addProject = () => {
    if (projectName.trim()) {
      setProjects([
        ...projects,
        {
          project_name: projectName.trim(),
          description: projectDescription,
          technologies_used: projectTechnologies.split(',').map(t => t.trim()).filter(t => t)
        }
      ])
      setProjectName('')
      setProjectDescription('')
      setProjectTechnologies('')
      toast.success('Project added')
    }
  }

  const removeProject = (index) => {
    setProjects(projects.filter((_, i) => i !== index))
  }

  const handleSubmit = () => {
    if (skills.length === 0 && projects.length === 0) {
      toast.error('Add at least one skill or project')
      return
    }
    onSave?.({ skills, projects })
  }

  const categoryPill = {
    technical: 'bg-blueprint-50 text-blueprint',
    soft: 'bg-success/10 text-success',
    domain: 'bg-gold-light text-gold-dark',
    tool: 'bg-ink/5 text-ink/70',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Skills Section */}
      <div className="blueprint-card rounded-xl p-8">
        <h2 className="text-xl font-display font-bold mb-1">Your skills</h2>
        <p className="text-ink/60 text-sm mb-6">
          Add your technical and soft skills. Be honest about your proficiency level.
        </p>

        <div className="bg-paper rounded-lg p-4 mb-6 border border-ink/5">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              placeholder="e.g., Python, React, Communication"
              className="input"
              onKeyPress={(e) => e.key === 'Enter' && addSkill()}
            />
            <select value={skillCategory} onChange={(e) => setSkillCategory(e.target.value)} className="input">
              <option value="technical">Technical</option>
              <option value="soft">Soft skill</option>
              <option value="domain">Domain knowledge</option>
              <option value="tool">Tool/software</option>
            </select>
            <div className="flex items-center gap-2">
              <input
                type="range"
                min="0"
                max="100"
                value={skillProficiency}
                onChange={(e) => setSkillProficiency(e.target.value)}
                className="flex-1 accent-blueprint"
              />
              <span className="metric-label w-12">{skillProficiency}%</span>
            </div>
          </div>
          <button onClick={addSkill} className="btn btn-secondary mt-3 w-full text-sm">
            + Add skill
          </button>
        </div>

        {skills.length > 0 ? (
          <div className="space-y-2">
            {skills.map((skill, index) => (
              <div key={index} className="flex items-center justify-between bg-white border border-ink/10 rounded-lg p-3">
                <div>
                  <p className="font-semibold text-sm">{skill.skill_name}</p>
                  <span className={`pill mt-1 ${categoryPill[skill.skill_category]}`}>{skill.skill_category}</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-24 progress-track">
                    <div className="progress-fill" style={{ width: `${skill.proficiency}%` }} />
                  </div>
                  <span className="metric-label">{skill.proficiency}%</span>
                  <button onClick={() => removeSkill(index)} className="text-danger hover:opacity-70">✕</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-ink/40 text-sm py-4">No skills added yet</p>
        )}
      </div>

      {/* Projects Section */}
      <div className="blueprint-card rounded-xl p-8">
        <h2 className="text-xl font-display font-bold mb-1">Your projects</h2>
        <p className="text-ink/60 text-sm mb-6">
          Add projects you've worked on — this helps us understand your practical experience.
        </p>

        <div className="bg-paper rounded-lg p-4 mb-6 border border-ink/5">
          <div className="space-y-3">
            <input
              type="text"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="Project name *"
              className="input"
            />
            <textarea
              value={projectDescription}
              onChange={(e) => setProjectDescription(e.target.value)}
              placeholder="Brief description of the project"
              className="input"
              rows="3"
            />
            <input
              type="text"
              value={projectTechnologies}
              onChange={(e) => setProjectTechnologies(e.target.value)}
              placeholder="Technologies used (comma separated) e.g., React, Node.js, MongoDB"
              className="input"
            />
            <button onClick={addProject} className="btn btn-secondary w-full text-sm">
              + Add project
            </button>
          </div>
        </div>

        {projects.length > 0 ? (
          <div className="space-y-2">
            {projects.map((project, index) => (
              <div key={index} className="bg-white border border-ink/10 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-display font-bold text-sm">{project.project_name}</h4>
                    {project.description && (
                      <p className="text-sm text-ink/60 mt-1">{project.description}</p>
                    )}
                  </div>
                  <button onClick={() => removeProject(index)} className="text-danger hover:opacity-70">✕</button>
                </div>
                {project.technologies_used?.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {project.technologies_used.map((tech, i) => (
                      <span key={i} className="pill bg-blueprint-50 text-blueprint">{tech}</span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-ink/40 text-sm py-4">No projects added yet</p>
        )}
      </div>

      <button onClick={handleSubmit} className="btn btn-primary w-full">
        Save skills & projects
      </button>
    </motion.div>
  )
}

export default SkillEntry
