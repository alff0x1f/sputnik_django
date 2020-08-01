import classNames from "classnames"
import React from "react"
import { Checkbox, PostValidationError, Timestamp } from "../../../../UI"
import { IMutationError } from "../../../../types"
import { IPost } from "../../Thread.types"

interface IThreadPostsModerationSelectedThreadListItemProps {
  disabled?: boolean
  error?: IMutationError
  id?: string
  selected?: boolean
  post: IPost
  changeSelection: (id: string, selected: boolean) => void
}

const ThreadPostsModerationSelectedThreadListItem: React.FC<IThreadPostsModerationSelectedThreadListItemProps> = ({
  disabled,
  error,
  id,
  selected,
  post,
  changeSelection,
}) => {
  const itemId = id ? id + "_" + post.id : undefined

  return (
    <li
      className={classNames("selected-item selected-post", {
        "is-invalid": !!error,
      })}
    >
      {error && (
        <PostValidationError error={error}>
          {({ message }) => (
            <div className="selected-item-error">{message}</div>
          )}
        </PostValidationError>
      )}
      <div className="row row-nogutters">
        <div className="col selected-item-body">
          <label className="selected-post-header" htmlFor={itemId}>
            <span className="selected-post-poster">
              {post.poster ? post.poster.name : post.posterName}
            </span>
            <span className="selected-post-timestamp">
              <Timestamp date={new Date(post.postedAt)} />
            </span>
          </label>
          <div className="selected-post-body">{post.body.text}</div>
        </div>
        <div className="col-auto selected-item-checkbox">
          <Checkbox
            checked={selected}
            disabled={disabled}
            id={itemId}
            onChange={(event) => {
              changeSelection(post.id, event.target.checked)
            }}
          />
        </div>
      </div>
    </li>
  )
}

export default ThreadPostsModerationSelectedThreadListItem
