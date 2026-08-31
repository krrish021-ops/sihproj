import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import { getStudentProfile, updateStudentProfile, addSkills } from '../services/studentService';
import AppShell from '../components/layout/AppShell';
import LoadingSpinner from '../components/common/LoadingSpinner';
import toast from 'react-hot-toast';

export default function ProfilePage() {
  const authUser = useSelector((state) => state.auth?.user);
  const userId = authUser?.id || JSON.parse(localStorage.getItem('user') || '{}')?.id || 1;

  const [loading, setLoading] = useState(true);
  const [profileData, setProfileData] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [showSkillModal, setShowSkillModal] = useState(false);

  const [formData, setFormData] = useState({
    phone: '', location: '', bio: '', education: '', institution: '', cgpa: '', linkedin: '',
  });

  const [newSkill, setNewSkill] = useState({ skill_name: '', proficiency: 70 });

  const loadProfile = async () => {
    setLoading(true);
    try {
      const data = await getStudentProfile(userId);
      if (data) {
        setProfileData(data);
        setFormData({
          phone: data.phone || '', location: data.location || '', bio: data.bio || '',
          education: data.education || '', institution: data.institution || '', cgpa: data.cgpa || '', linkedin: data.linkedin || '',
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadProfile(); }, [userId]);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateStudentProfile(userId, formData);
      toast.success('Profile updated successfully!');
      setIsEditing(false);
      loadProfile();
    } catch (err) {
      toast.error('Failed to update profile.');
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    if (!newSkill.skill_name.trim()) return toast.error('Please enter a skill name.');
    try {
      await addSkills(userId, { skill_name: newSkill.skill_name.trim(), proficiency: Number(newSkill.proficiency) });
      toast.success(`Added ${newSkill.skill_name}!`);
      setShowSkillModal(false);
      setNewSkill({ skill_name: '', proficiency: 70 });
      loadProfile();
    } catch (err) {
      toast.error('Failed to add skill.');
    }
  };

  const fullName = profileData?.user?.full_name || authUser?.full_name || 'Student';
  const email = profileData?.user?.email || authUser?.email || '';
  const skillsList = Array.isArray(profileData?.skills) ? profileData.skills : Array.isArray(profileData?.student_skills) ? profileData.student_skills : [];
  const projectsList = Array.isArray(profileData?.projects) ? profileData.projects : Array.isArray(profileData?.student_projects) ? profileData.student_projects : [];

  return (
    <AppShell>
      <div className="max-w-5xl mx-auto space-y-6 p-6">
        {loading ? (
          <div className="py-20 flex justify-center"><LoadingSpinner text="Loading Profile..." /></div>
        ) : (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
            
            {/* Header Blueprint Card */}
            <div className="blueprint-card p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-[#0E2A47] text-white flex items-center justify-center text-2xl font-bold font-['Space_Grotesk']">
                  {fullName.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-[#12202B] font-['Space_Grotesk']">{fullName}</h1>
                  <p className="text-gray-600">{email}</p>
                </div>
              </div>
              <button onClick={() => setIsEditing(true)} className="btn-secondary shrink-0">
                Edit Profile
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column */}
              <div className="space-y-6 lg:col-span-1">
                <div className="blueprint-card p-5">
                  <h3 className="font-mono text-sm uppercase text-gray-500 mb-4 tracking-wider">Academic Profile</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <p className="text-gray-500 font-mono text-xs">INSTITUTION</p>
                      <p className="font-medium text-[#12202B]">{profileData?.institution || 'Not set'}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 font-mono text-xs">DEGREE</p>
                      <p className="font-medium text-[#12202B]">{profileData?.education || 'Not set'}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 font-mono text-xs">CGPA</p>
                      <p className="font-medium text-[#12202B]">{profileData?.cgpa || 'Not set'}</p>
                    </div>
                  </div>
                </div>

                <div className="blueprint-card p-5">
                  <h3 className="font-mono text-sm uppercase text-gray-500 mb-3 tracking-wider">Bio</h3>
                  <p className="text-sm text-gray-700 leading-relaxed">{profileData?.bio || 'No bio provided.'}</p>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6 lg:col-span-2">
                
                {/* Skills */}
                <div className="blueprint-card p-6">
                  <div className="flex justify-between items-center mb-5">
                    <h3 className="font-mono text-sm uppercase text-gray-500 tracking-wider">Technical Skills</h3>
                    <button onClick={() => setShowSkillModal(true)} className="btn-secondary text-xs px-3 py-1">
                      + Add Skill
                    </button>
                  </div>
                  {skillsList.length === 0 ? (
                    <p className="text-gray-500 text-sm">No skills added yet.</p>
                  ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {skillsList.map((s, i) => {
                        const isVerified = s.is_verified || s.source === 'assessment_verified';
                        const prof = s.proficiency || 50;
                        return (
                          <div key={i} className="p-3 border border-gray-100 rounded-lg">
                            <div className="flex justify-between items-center mb-2">
                              <span className="font-medium text-sm text-[#12202B] flex items-center gap-2">
                                {s.skill_name || s.skill || ''}
                                {isVerified && <span className="pill bg-[#D9A441]/20 text-[#B8842E] text-[10px] px-1.5 py-0.5">Verified</span>}
                              </span>
                              <span className="font-mono text-xs text-[#0E2A47]">{prof}%</span>
                            </div>
                            <div className="progress-track bg-gray-100 h-1.5 rounded-full w-full overflow-hidden">
                              <div className="progress-fill bg-[#0E2A47] h-full rounded-full" style={{ width: `${prof}%` }}></div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Projects */}
                <div className="blueprint-card p-6">
                  <h3 className="font-mono text-sm uppercase text-gray-500 mb-5 tracking-wider">Projects</h3>
                  {projectsList.length === 0 ? (
                    <p className="text-gray-500 text-sm">No projects added yet.</p>
                  ) : (
                    <div className="space-y-4">
                      {projectsList.map((p, i) => (
                        <div key={i} className="pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                          <h4 className="font-bold text-[#12202B] text-sm">{p.project_name || p.title}</h4>
                          <p className="text-sm text-gray-600 mt-1">{p.description}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Modals */}
        <AnimatePresence>
          {isEditing && (
            <div className="fixed inset-0 bg-[#12202B]/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
              <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }} className="blueprint-card w-full max-w-lg p-6 max-h-[90vh] overflow-y-auto">
                <h2 className="text-xl font-bold font-['Space_Grotesk'] text-[#0E2A47] mb-4">Edit Profile</h2>
                <form onSubmit={handleProfileSubmit} className="space-y-4 text-sm">
                  <div><label className="block text-gray-600 mb-1">Institution</label><input type="text" className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-[#0E2A47]" value={formData.institution} onChange={(e)=>setFormData({...formData, institution: e.target.value})} /></div>
                  <div><label className="block text-gray-600 mb-1">Degree</label><input type="text" className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-[#0E2A47]" value={formData.education} onChange={(e)=>setFormData({...formData, education: e.target.value})} /></div>
                  <div><label className="block text-gray-600 mb-1">CGPA</label><input type="text" className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-[#0E2A47]" value={formData.cgpa} onChange={(e)=>setFormData({...formData, cgpa: e.target.value})} /></div>
                  <div><label className="block text-gray-600 mb-1">Bio</label><textarea className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-[#0E2A47]" rows="3" value={formData.bio} onChange={(e)=>setFormData({...formData, bio: e.target.value})}></textarea></div>
                  <div className="flex justify-end gap-3 pt-4">
                    <button type="button" onClick={() => setIsEditing(false)} className="btn-secondary">Cancel</button>
                    <button type="submit" className="btn-primary">Save Changes</button>
                  </div>
                </form>
              </motion.div>
            </div>
          )}

          {showSkillModal && (
            <div className="fixed inset-0 bg-[#12202B]/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
              <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }} className="blueprint-card w-full max-w-md p-6">
                <h2 className="text-xl font-bold font-['Space_Grotesk'] text-[#0E2A47] mb-4">Add Skill</h2>
                <form onSubmit={handleAddSkill} className="space-y-4 text-sm">
                  <div>
                    <label className="block text-gray-600 mb-1">Skill Name</label>
                    <input type="text" placeholder="e.g. React" className="w-full border border-gray-300 p-2 rounded focus:outline-none focus:border-[#0E2A47]" value={newSkill.skill_name} onChange={(e)=>setNewSkill({...newSkill, skill_name: e.target.value})} />
                  </div>
                  <div>
                    <div className="flex justify-between text-gray-600 mb-1"><label>Proficiency</label><span className="font-mono">{newSkill.proficiency}%</span></div>
                    <input type="range" min="10" max="100" className="w-full accent-[#0E2A47]" value={newSkill.proficiency} onChange={(e)=>setNewSkill({...newSkill, proficiency: e.target.value})} />
                  </div>
                  <div className="flex justify-end gap-3 pt-4">
                    <button type="button" onClick={() => setShowSkillModal(false)} className="btn-secondary">Cancel</button>
                    <button type="submit" className="btn-primary">Add Skill</button>
                  </div>
                </form>
              </motion.div>
            </div>
          )}
        </AnimatePresence>
      </div>
    </AppShell>
  );
}