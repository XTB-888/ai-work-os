import * as React from 'react'
import { cn } from '@/lib/utils'

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number
  max?: number
  showLabel?: boolean
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, max = 100, showLabel = false, ...props }, ref) => {
    const percentage = Math.min(Math.max((value / max) * 100, 0), 100)

    return (
      <div className={cn('relative', className)} ref={ref} {...props}>
        <div className="overflow-hidden h-2 rounded-full bg-gray-200">
          <div
            className={cn(
              'h-full rounded-full transition-all duration-500 ease-out',
              percentage >= 100
                ? 'bg-green-500'
                : percentage >= 60
                ? 'bg-blue-500'
                : percentage >= 30
                ? 'bg-yellow-500'
                : 'bg-red-500'
            )}
            style={{ width: `${percentage}%` }}
          />
        </div>
        {showLabel && (
          <span className="absolute right-0 top-0 -mt-5 text-xs text-gray-600">
            {Math.round(percentage)}%
          </span>
        )}
      </div>
    )
  }
)
Progress.displayName = 'Progress'

export { Progress }
