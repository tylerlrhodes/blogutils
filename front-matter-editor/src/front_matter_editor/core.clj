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
  [file-name]
  (try
    {:file-name file-name
     :front-matter
     (let [result
           (with-open [rdr (reader file-name)]
             (reduce
              #(if (and
                    (not (nil? %2))
                    (= %2 "---"))
                 (if (= 1 (:marker %1))
                   (reduced
                    (string/join "\n" (:lines %1)))
                   {:marker (inc (:marker %1))
                    :lines  (:lines %1)})
                 {:marker (:marker %1)
                  :lines  (conj (apply vector (:lines %1)) %2)})
              {:marker 0 :lines nil}
              (line-seq rdr)))]
       (if (map? result)
         nil
         result))}
    (catch Exception e
      println e)))

(defn get-yaml
  [entry]
  (if-let [front-matter (:front-matter entry)]
    (assoc entry
           :yaml
           (yaml/parse-string front-matter))
    (assoc entry
           :yaml nil)))

(defn needs-meta-fix?
  [entry]
  (assoc entry
         :needs-fix
         (if-let [yaml (:yaml entry)]
           (not
            (and
             (:description yaml)
             (:keywords yaml)
             (:tags yaml)))    
           false)))

(defn get-files
  [directory]
  (try
    (remove
     (fn
       [path]
       (if (string/ends-with? (string/lower-case path)
                              ".md")
         false
         true))
     (map
      (fn
        [file]
        (.getPath file))
      (file-seq (file directory))))
    (catch Exception e
      println e)))

(defn print-entry
  [entry]
  (clojure.pprint/pprint entry))

(defn get-new-meta
  [entry]
  (let [yaml (:yaml entry)]
    (let [yaml (assoc yaml
                      :description
                      (do
                        (println "Enter Description: ")
                        (read-line)))]
      (let [yaml (assoc yaml
                        :keywords
                        (do
                          (println "Enter Keywords: ")
                          (apply list (string/split (read-line) #" "))))]
        (let [yaml (assoc yaml
                          :tags
                          (do
                            (println "Enter Tags: ")
                            (apply list (string/split (read-line) #" "))))]
          (assoc entry
                 :yaml
                 yaml))))))

(defn program
  []
  (let [entries
        (filter
         #(:needs-fix %1)
         (map
          (comp needs-meta-fix? get-yaml get-front-matter)
          (get-files "C:\\temp\\blog2\\content\\posts\\")))]
    (loop [entries entries
           term ""]
      (if (or
           (empty? entries)
           (= term "q"))
        true
        (do
          (println "Existing entry: \n")
          (print-entry (first entries))
          (let [updated-entry (get-new-meta (first entries))]
            (println "\n\nUpdated Entry:")
            (print-entry updated-entry)
            (println "\nr to redo, n to continue, q to quit:")
            (recur (rest entries) (str (read)))))))))


        

