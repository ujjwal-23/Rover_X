
(cl:in-package :asdf)

(defsystem "realsense2_camera-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Drive" :depends-on ("_package_Drive"))
    (:file "_package_Drive" :depends-on ("_package"))
    (:file "Extrinsics" :depends-on ("_package_Extrinsics"))
    (:file "_package_Extrinsics" :depends-on ("_package"))
    (:file "IMUInfo" :depends-on ("_package_IMUInfo"))
    (:file "_package_IMUInfo" :depends-on ("_package"))
    (:file "Metadata" :depends-on ("_package_Metadata"))
    (:file "_package_Metadata" :depends-on ("_package"))
    (:file "Middle_list" :depends-on ("_package_Middle_list"))
    (:file "_package_Middle_list" :depends-on ("_package"))
  ))