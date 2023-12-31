#pragma once

#include "Eigen/Dense"

#include "hebi_cpp_api/robot_model.hpp"

namespace hebi {
namespace experimental {
namespace arm {
namespace internal {

// A small helper class for computing IK and storing preferences about how this is done.
class KinematicsHelper {

public:
  void setJointLimits(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& min_positions,
    const Eigen::VectorXd& max_positions);

  void clearJointLimits();

  Eigen::Vector3d FK3Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& positions) const;

  void FK5Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& positions,
    Eigen::Vector3d& xyz_out,
    Eigen::Vector3d& tip_axis) const;

  void FK6Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& positions,
    Eigen::Vector3d& xyz_out,
    Eigen::Matrix3d& orientation) const;

  Eigen::VectorXd solveIK3Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& initial_positions,
    const Eigen::Vector3d& target_xyz) const;

  Eigen::VectorXd solveIK5Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& initial_positions,
    const Eigen::Vector3d& target_xyz,
    const Eigen::Vector3d& end_tip) const;

  Eigen::VectorXd solveIK6Dof(
    const robot_model::RobotModel& robot_model,
    const Eigen::VectorXd& initial_positions,
    const Eigen::Vector3d& target_xyz,
    const Eigen::Matrix3d& orientation) const;

private:
  bool use_joint_limits_{};
  Eigen::VectorXd min_positions_{};
  Eigen::VectorXd max_positions_{};
};

} // namespace internal
} // namespace arm
} // namespace experimental
} // namespace hebi
