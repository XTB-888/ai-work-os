import React from 'react'

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  text?: string
}

export function LoadingSpinner({ size = 'md', text }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div
        className={`${sizeClasses[size]} animate-spin rounded-full border-b-2 border-blue-600`}
      />
      {text && <p className="mt-4 text-gray-600">{text}</p>}
    </div>
  )
}

interface LoadingOverlayProps {
  text?: string
}

export function LoadingOverlay({ text = 'Loading...' }: LoadingOverlayProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8">
        <LoadingSpinner size="lg" text={text} />
      </div>
    </div>
  )
}

interface PageLoadingProps {
  text?: string
}

export function PageLoading({ text = 'Loading...' }: PageLoadingProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <LoadingSpinner size="lg" text={text} />
    </div>
  )
}
