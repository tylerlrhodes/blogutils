(ns front-matter-editor.core
  (:gen-class)
  (:require [clojure.java.io :refer :all]
            [clojure.string :as string]
            [clj-yaml.core :as yaml]))

;; This program should:
;; for each file in a directory, if it is markdown, get the front-matter
;; and build a list of all the entries that need to be udpated
;; for each entry that needs updating, prompt the user for the missing
;; meta tags

(defn get-front-matter
  [fn]
  (try
    {:fn fn
     :front-matter
     (let [result
           (with-open [rdr (reader fn)]
             (reduce
              #(if (and
                    (not (nil? %2))
                    (= %2 "---"))
                 (if (= 1 (:marker %1))
                   (reduced
                    (string/join "\n" (reverse (:lines %1))))
                   {:marker (inc (:marker %1))
                    :lines  (:lines %1)})
                 {:marker (:marker %1)
                  :lines  (conj (:lines %1) %2)})
              {:marker 0 :lines nil}
              (line-seq rdr)))]
       (if (map? result)
         nil
         result))}
    (catch Exception e
      println e)))

(defn needs-meta-fix?
  [front-matter]
  true)

(defn do-stuff
  [dir]
  (let [to-update (remove nil? (map (comp needs-meta-fix? get-front-matter (fn [f] (.getPath f))) (file-seq (file dir))))]
    to-update))




