import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { motion } from 'framer-motion'
import { startAssessment, submitAnswer } from '../services/assessmentService'
import AppShell from '../components/layout/AppShell'
import AssessmentInterface from '../components/student/AssessmentInterface'
import SkillReport from '../components/student/SkillReport'
import toast from 'react-hot-toast'

const AssessmentPage = () => {
  const { user } = useSelector(state => state.auth)
  const [state, setState] = useState(null)
  const [question, setQuestion] = useState(null)
  const [loading, setLoading] = useState(false)
  const [complete, setComplete] = useState(false)
  const [report, setReport] = useState(null)
  const [questionNum, setQuestionNum] = useState(0)

  const start = async () => {
    setLoading(true)
    try {
      const response = await startAssessment(user.id)
      setState(response.state)
      setQuestion(response.question)
    } catch (error) {
      toast.error('Failed to start assessment')
    } finally {
      setLoading(false)
    }
  }

  const submit = async (answer) => {
    setLoading(true)
    try {
      const response = await submitAnswer({ state, answer })
      if (response.complete) {
        setComplete(true)
        setReport(response.report)
        toast.success('Assessment complete!')
      } else {
        setState(response.state)
        setQuestion(response.question)
        setQuestionNum(prev => prev + 1)
      }
    } catch (error) {
      toast.error('Failed to submit')
    } finally {
      setLoading(false)
    }
  }

  if (!question && !complete) {
    return (
      <AppShell>
        <div className="min-h-[70vh] flex items-center justify-center p-8">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="blueprint-card rounded-xl p-10 text-center max-w-md"
          >
            <h2 className="text-xl font-display font-bold mb-2">Ready for your skill assessment?</h2>
            <p className="text-ink/60 text-sm mb-6">
              10 adaptive questions, one at a time. Your answers shape what comes next.
            </p>
            <button onClick={start} disabled={loading} className="btn btn-primary">
              {loading ? 'Starting…' : 'Start assessment'}
            </button>
          </motion.div>
        </div>
      </AppShell>
    )
  }

  if (complete && report) {
    return (
      <AppShell>
        <div className="max-w-2xl mx-auto p-8">
          <SkillReport report={report} />
        </div>
      </AppShell>
    )
  }

  return (
    <AppShell>
      <div className="p-8">
        <AssessmentInterface
          question={question}
          questionNumber={questionNum + 1}
          totalQuestions={state?.max_questions || 10}
          onSubmit={submit}
          loading={loading}
        />
      </div>
    </AppShell>
  )
}

export default AssessmentPage
