import { ApolloError } from "apollo-client"
import React from "react"
import {
  PostValidationError,
  RootError,
  ThreadValidationError,
  useLocationError,
  useRootError,
} from "../../../../UI"
import { IMutationError } from "../../../../types"

interface IRootError {
  message: React.ReactNode
  type: string
}

interface IThreadPostRootErrorProps {
  children: (error: IRootError) => React.ReactElement
  dataErrors?: Array<IMutationError> | null
  graphqlError?: ApolloError | null
}

const ThreadPostRootError: React.FC<IThreadPostRootErrorProps> = ({
  children,
  dataErrors,
  graphqlError,
}) => {
  const rootError = useRootError(dataErrors)
  const threadError = useLocationError("thread", dataErrors)
  const postError = useLocationError("post", dataErrors)

  if (graphqlError) {
    return <RootError graphqlError={graphqlError}>{children}</RootError>
  }

  if (rootError) {
    return <RootError dataErrors={[rootError]}>{children}</RootError>
  }

  if (threadError) {
    return (
      <ThreadValidationError error={threadError}>
        {children}
      </ThreadValidationError>
    )
  }

  if (postError) {
    return (
      <PostValidationError error={postError}>{children}</PostValidationError>
    )
  }

  return null
}

export default ThreadPostRootError