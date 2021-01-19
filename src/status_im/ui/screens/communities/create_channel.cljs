(ns status-im.ui.screens.communities.create-channel
  (:require [clojure.string :as str]
            [reagent.core :as reagent]
            [quo.react-native :as rn]
            [quo.core :as quo]
            [status-im.i18n :as i18n]
            [status-im.ui.components.toolbar :as toolbar]
            [re-frame.core :as re-frame]
            [status-im.communities.core :as communities]
            [status-im.ui.components.topbar :as topbar]))

(defn valid? [community-name community-description]
  (and (not (str/blank? community-name))
       (not (str/blank? community-description))))

(defn create-channel []
  (let [channel-name        (reagent/atom "")
        channel-description (reagent/atom "")]
    (fn []
      [:<>
       [topbar/topbar {:title (i18n/label :t/create-channel-title)}]
       [rn/scroll-view {:style                   {:flex 1}
                        :content-container-style {:padding-vertical 16}}
        [rn/view {:style {:padding-bottom     16
                          :padding-top        10
                          :padding-horizontal 16}}
         [quo/text-input
          {:label          (i18n/label :t/name-your-channel)
           :placeholder    (i18n/label :t/name-your-channel-placeholder)
           :on-change-text #(reset! channel-name %)
           :auto-focus     true}]]
        [rn/view {:style {:padding-bottom     16
                          :padding-top        10
                          :padding-horizontal 16}}
         [quo/text-input
          {:label           (i18n/label :t/give-a-short-description-channel)
           :placeholder     (i18n/label :t/give-a-short-description-channel)
           :multiline       true
           :number-of-lines 4
           :on-change-text  #(reset! channel-description %)}]]]
       [toolbar/toolbar
        {:show-border? true
         :center
         [quo/button {:disabled (not (valid? @channel-name @channel-description))
                      :type     :secondary
                      :on-press #(re-frame/dispatch [::communities/create-channel-confirmation-pressed @channel-name @channel-description])}
          (i18n/label :t/create)]}]])))
