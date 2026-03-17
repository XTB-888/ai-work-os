import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ErrorBoundary } from '@/components/ErrorBoundary'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AI Work OS - Transform Goals into Results',
  description: 'AI-powered work operating system with multi-agent collaboration. Transform your goals into tangible results through autonomous AI agent teams.',
  keywords: 'AI, agents, automation, workflow, LangGraph, FastAPI, Next.js',
  authors: [{ name: 'AI Work OS Team' }],
  openGraph: {
    title: 'AI Work OS',
    description: 'Transform Goals into Results with AI Agent Teams',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
      </body>
    </html>
  )
}
