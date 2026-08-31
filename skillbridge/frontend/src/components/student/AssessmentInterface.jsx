// Assessment Interface Component
import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const AssessmentInterface = ({ question, questionNumber, totalQuestions, onSubmit, loading }) => {
  const [selectedAnswer, setSelectedAnswer] = useState('')
  const [timeLeft, setTimeLeft] = useState(60)

  useEffect(() => {
    setSelectedAnswer('')
    setTimeLeft(60)
  }, [question])

  useEffect(() => {
    if (timeLeft > 0 && !loading) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [timeLeft, loading])

  const handleSubmit = () => {
    if (selectedAnswer && !loading) {
      onSubmit(selectedAnswer)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="metric-label uppercase">
            Question {questionNumber} of {totalQuestions}
          </span>
          <span className={`metric-label ${timeLeft <= 10 ? 'text-danger' : ''}`}>
            {timeLeft}s
          </span>
        </div>
        <div className="progress-track">
          <div
            className="progress-fill"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
      </div>

      {/* Question Card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={questionNumber}
          initial={{ opacity: 0, x: 40 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -40 }}
          transition={{ duration: 0.25 }}
          className="blueprint-card rounded-xl p-8"
        >
          <div className="mb-6">
            <div className="flex gap-2 mb-4">
              <span className="pill bg-blueprint-50 text-blueprint">{question?.skill}</span>
              <span className="pill bg-gold-light text-gold-dark">{question?.difficulty}</span>
            </div>
            <h3 className="text-xl font-display font-bold text-ink">
              {question?.question}
            </h3>
          </div>

          <div className="space-y-3 mb-6">
            {question?.options?.map((option, index) => (
              <button
                key={index}
                onClick={() => setSelectedAnswer(option)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-all duration-150 ${
                  selectedAnswer === option
                    ? 'border-blueprint bg-blueprint-50'
                    : 'border-ink/10 hover:border-ink/25'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className={`w-8 h-8 rounded-full flex items-center justify-center font-display font-bold text-sm ${
                    selectedAnswer === option
                      ? 'bg-blueprint text-white'
                      : 'bg-ink/5 text-ink/50'
                  }`}>
                    {String.fromCharCode(65 + index)}
                  </span>
                  <span className="font-medium">{option}</span>
                </div>
              </button>
            ))}
          </div>

          <button
            onClick={handleSubmit}
            disabled={!selectedAnswer || loading}
            className="btn btn-primary w-full"
          >
            {loading ? 'Submitting…' : 'Submit answer'}
          </button>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}

export default AssessmentInterface
