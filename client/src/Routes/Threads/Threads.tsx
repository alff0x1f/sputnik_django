import React from "react"
import { Route, Switch } from "react-router-dom"
import { useSettingsContext } from "../../Context"
import { RouteErrorBoundary, RouteLoader, RouteNotFound } from "../../UI"
import * as urls from "../../urls"
import {
  ThreadsCategoriesModal,
  ThreadsCategoriesModalContextProvider,
} from "./ThreadsCategoriesModal"
import ThreadsCategoryRoute from "./ThreadsCategoryRoute"
import {
  ThreadsModerationModalClose,
  ThreadsModerationModalContextProvider,
  ThreadsModerationModalDelete,
  ThreadsModerationModalMove,
  ThreadsModerationModalOpen,
} from "./ThreadsModeration"
import ThreadsRoute from "./ThreadsRoute"

const Threads: React.FC = () => {
  const settings = useSettingsContext()

  return (
    <ThreadsModerationModalContextProvider>
      <ThreadsModerationModalOpen />
      <ThreadsModerationModalClose />
      <ThreadsModerationModalDelete />
      <ThreadsModerationModalMove />
      <ThreadsCategoriesModalContextProvider>
        <ThreadsCategoriesModal />
        <Switch>
          <Route
            path={urls.category({ id: ":id", slug: ":slug" })}
            render={() => (
              <RouteErrorBoundary>
                <ThreadsCategoryRoute />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={settings?.forumIndexThreads ? urls.index() : urls.threads()}
            render={() => (
              <RouteErrorBoundary>
                <ThreadsRoute />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={urls.index()}
            render={() => (settings ? <RouteNotFound /> : <RouteLoader />)}
          />
        </Switch>
      </ThreadsCategoriesModalContextProvider>
    </ThreadsModerationModalContextProvider>
  )
}

export default Threads