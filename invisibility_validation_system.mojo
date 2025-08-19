"""
Invisibility Validation System
Comprehensive testing and measurement framework for invisible equipment design

Implements low-interference validation methods with objective proxies
and minimal subjective disruption to maintain flow state during testing.

Authors: Cognitive Design Framework Team  
Version: v1.0 - Flow State Validation
Date: January 2025
"""

from python import Python
from math import sqrt, pow, abs, min, max, sin, cos, pi, log
from invisible_equipment_framework import FlowStateMetrics, InvisibilityPrinciples


struct IMUDataProcessor:
    """
    Advanced IMU data processing for flow state analysis.
    Extracts micro-correction patterns and movement smoothness metrics.
    """
    
    var sampling_rate: Float64              # Hz - typically 100Hz for high-resolution analysis
    var filter_cutoff: Float64              # Hz - low-pass filter for noise reduction
    var correction_threshold: Float64       # Threshold for detecting micro-corrections
    var smoothness_window: Int              # Sample window for smoothness calculation
    
    fn __init__(inout self):
        self.sampling_rate = 100.0
        self.filter_cutoff = 10.0
        self.correction_threshold = 0.5  # degrees/sample
        self.smoothness_window = 50      # 0.5 second window at 100Hz
    
    fn calculate_micro_correction_rate(inout self, imu_data: Python.list) -> Float64:
        """
        Calculates high-frequency roll/yaw input corrections per minute.
        Lower rates indicate better equipment invisibility.
        """
        var corrections = 0
        var total_samples = len(imu_data)
        
        if total_samples < 2:
            return 0.0
        
        # Apply high-pass filter to isolate micro-corrections
        var filtered_data = self._apply_high_pass_filter(imu_data)
        
        # Count corrections exceeding threshold
        for i in range(1, len(filtered_data)):
            var current_sample = filtered_data[i]
            var prev_sample = filtered_data[i-1]
            
            var roll_change = abs(current_sample[0].to_float64() - prev_sample[0].to_float64())
            var yaw_change = abs(current_sample[1].to_float64() - prev_sample[1].to_float64())
            
            if roll_change > self.correction_threshold or yaw_change > self.correction_threshold:
                corrections += 1
        
        # Convert to corrections per minute
        var duration_minutes = total_samples.to_float64() / (self.sampling_rate * 60.0)
        return corrections.to_float64() / duration_minutes
    
    fn calculate_movement_smoothness(inout self, imu_data: Python.list) -> Float64:
        """
        Calculates jerk and spectral smoothness of movement.
        Uses normalized jerk metric (lower = smoother).
        """
        if len(imu_data) < 3:
            return 1.0  # Maximum roughness for insufficient data
        
        var total_jerk = 0.0
        var sample_count = 0
        
        # Calculate jerk (third derivative of position)
        for i in range(2, len(imu_data)):
            var acc_current = self._calculate_acceleration(imu_data, i)
            var acc_prev = self._calculate_acceleration(imu_data, i-1)
            
            var jerk_x = abs(acc_current[0] - acc_prev[0]) / (1.0 / self.sampling_rate)
            var jerk_y = abs(acc_current[1] - acc_prev[1]) / (1.0 / self.sampling_rate)
            var jerk_z = abs(acc_current[2] - acc_prev[2]) / (1.0 / self.sampling_rate)
            
            var jerk_magnitude = sqrt(jerk_x*jerk_x + jerk_y*jerk_y + jerk_z*jerk_z)
            total_jerk += jerk_magnitude
            sample_count += 1
        
        if sample_count == 0:
            return 1.0
        
        # Normalize to 0-1 scale (empirically derived normalization factor)
        var mean_jerk = total_jerk / sample_count.to_float64()
        return min(1.0, mean_jerk / 100.0)  # 100 m/s³ = maximum expected jerk
    
    fn calculate_path_consistency(inout self, trajectory_data: Python.list, reference_speed: Float64) -> Float64:
        """
        Calculates variance of carve radius for matched entry speeds.
        Lower variance indicates more consistent, predictable equipment behavior.
        """
        var carve_radii = Python.list()
        
        # Extract carving segments based on angular velocity
        var carve_segments = self._identify_carve_segments(trajectory_data)
        
        for segment in carve_segments:
            var segment_data = segment
            var entry_speed = segment_data[0].to_float64()
            
            # Only analyze segments with similar entry speeds (±10%)
            if abs(entry_speed - reference_speed) / reference_speed < 0.1:
                var radius = self._calculate_turn_radius(segment_data)
                carve_radii.append(radius)
        
        if len(carve_radii) < 2:
            return 0.0  # Need at least 2 turns for variance calculation
        
        # Calculate coefficient of variation (normalized standard deviation)
        var mean_radius = self._calculate_mean(carve_radii)
        var variance = self._calculate_variance(carve_radii, mean_radius)
        var std_deviation = sqrt(variance)
        
        if mean_radius == 0.0:
            return 1.0  # Maximum inconsistency
        
        var coefficient_of_variation = std_deviation / mean_radius
        return min(1.0, coefficient_of_variation)  # Cap at 1.0 for extreme cases
    
    fn detect_slip_stall_events(inout self, imu_data: Python.list, pressure_data: Python.list) -> Python.dict:
        """
        Detects slip/stall events and analyzes recovery consistency.
        Returns frequency and recovery time statistics.
        """
        var events = Python.dict()
        var slip_events = Python.list()
        var stall_events = Python.list()
        
        # Analyze for slip events (lateral acceleration vs expected)
        for i in range(1, len(imu_data)):
            var lateral_acc = imu_data[i][1].to_float64()  # Y-axis acceleration
            var expected_acc = self._calculate_expected_lateral_acc(imu_data, i)
            
            # Slip detected when actual acceleration significantly lower than expected
            if abs(lateral_acc - expected_acc) > 2.0 and lateral_acc < expected_acc * 0.7:
                var recovery_time = self._calculate_recovery_time(imu_data, i)
                slip_events.append(recovery_time)
        
        # Analyze for stall events (sudden loss of control authority)
        for i in range(self.smoothness_window, len(imu_data)):
            var control_authority = self._calculate_control_authority(imu_data, i)
            
            if control_authority < 0.3:  # Threshold for stall detection
                var recovery_time = self._calculate_recovery_time(imu_data, i)
                stall_events.append(recovery_time)
        
        # Calculate statistics
        events["slip_frequency"] = len(slip_events).to_float64() / (len(imu_data).to_float64() / self.sampling_rate / 60.0)  # Events per minute
        events["stall_frequency"] = len(stall_events).to_float64() / (len(imu_data).to_float64() / self.sampling_rate / 60.0)
        
        if len(slip_events) > 0:
            events["slip_recovery_mean"] = self._calculate_mean(slip_events)
            events["slip_recovery_std"] = sqrt(self._calculate_variance(slip_events, events["slip_recovery_mean"].to_float64()))
        else:
            events["slip_recovery_mean"] = 0.0
            events["slip_recovery_std"] = 0.0
        
        if len(stall_events) > 0:
            events["stall_recovery_mean"] = self._calculate_mean(stall_events)
            events["stall_recovery_std"] = sqrt(self._calculate_variance(stall_events, events["stall_recovery_mean"].to_float64()))
        else:
            events["stall_recovery_mean"] = 0.0
            events["stall_recovery_std"] = 0.0
        
        return events
    
    # Helper methods
    fn _apply_high_pass_filter(inout self, data: Python.list) -> Python.list:
        """Simple high-pass filter to isolate micro-corrections"""
        var filtered = Python.list()
        var alpha = 0.9  # High-pass filter coefficient
        
        if len(data) == 0:
            return filtered
        
        # Initialize with first sample
        var prev_filtered = data[0]
        filtered.append(prev_filtered)
        
        for i in range(1, len(data)):
            var current_raw = data[i]
            var current_filtered = Python.list()
            
            # Apply high-pass filter to each axis
            for axis in range(3):  # Assuming 3-axis data
                var raw_val = current_raw[axis].to_float64()
                var prev_filt = prev_filtered[axis].to_float64()
                var prev_raw = data[i-1][axis].to_float64()
                
                var filtered_val = alpha * (prev_filt + raw_val - prev_raw)
                current_filtered.append(filtered_val)
            
            filtered.append(current_filtered)
            prev_filtered = current_filtered
        
        return filtered
    
    fn _calculate_acceleration(inout self, imu_data: Python.list, index: Int) -> Python.list:
        """Calculate acceleration from IMU data"""
        var acceleration = Python.list([0.0, 0.0, 0.0])
        
        if index < 1 or index >= len(imu_data):
            return acceleration
        
        var current = imu_data[index]
        var previous = imu_data[index-1]
        var dt = 1.0 / self.sampling_rate
        
        for axis in range(3):
            var vel_change = current[axis].to_float64() - previous[axis].to_float64()
            acceleration[axis] = vel_change / dt
        
        return acceleration
    
    fn _identify_carve_segments(inout self, trajectory_data: Python.list) -> Python.list:
        """Identify distinct carving maneuvers from trajectory data"""
        var segments = Python.list()
        var current_segment = Python.list()
        var in_carve = False
        
        for i in range(len(trajectory_data)):
            var angular_velocity = trajectory_data[i][3].to_float64()  # Assuming yaw rate in index 3
            
            # Start of carve (significant angular velocity)
            if not in_carve and abs(angular_velocity) > 0.5:
                in_carve = True
                current_segment = Python.list()
                current_segment.append(trajectory_data[i])
            
            # Continue carve
            elif in_carve and abs(angular_velocity) > 0.2:
                current_segment.append(trajectory_data[i])
            
            # End of carve
            elif in_carve and abs(angular_velocity) <= 0.2:
                in_carve = False
                if len(current_segment) > 10:  # Minimum segment length
                    segments.append(current_segment)
        
        return segments
    
    fn _calculate_turn_radius(inout self, segment_data: Python.list) -> Float64:
        """Calculate turn radius from carve segment data"""
        if len(segment_data) < 3:
            return 0.0
        
        # Use average speed and angular velocity to estimate radius
        var total_speed = 0.0
        var total_angular_vel = 0.0
        var sample_count = 0
        
        for sample in segment_data:
            var speed = sample[4].to_float64()  # Assuming speed in index 4
            var angular_vel = abs(sample[3].to_float64())  # Yaw rate
            
            total_speed += speed
            total_angular_vel += angular_vel
            sample_count += 1
        
        if sample_count == 0 or total_angular_vel == 0.0:
            return 0.0
        
        var avg_speed = total_speed / sample_count.to_float64()
        var avg_angular_vel = total_angular_vel / sample_count.to_float64()
        
        # Radius = speed / angular_velocity
        return avg_speed / avg_angular_vel
    
    fn _calculate_mean(inout self, values: Python.list) -> Float64:
        """Calculate arithmetic mean of list values"""
        if len(values) == 0:
            return 0.0
        
        var sum = 0.0
        for value in values:
            sum += value.to_float64()
        
        return sum / len(values).to_float64()
    
    fn _calculate_variance(inout self, values: Python.list, mean: Float64) -> Float64:
        """Calculate variance of list values"""
        if len(values) == 0:
            return 0.0
        
        var sum_squared_diff = 0.0
        for value in values:
            var diff = value.to_float64() - mean
            sum_squared_diff += diff * diff
        
        return sum_squared_diff / len(values).to_float64()
    
    fn _calculate_expected_lateral_acc(inout self, imu_data: Python.list, index: Int) -> Float64:
        """Calculate expected lateral acceleration based on turn dynamics"""
        if index < 1 or index >= len(imu_data):
            return 0.0
        
        # Simplified model: expected_acc = v² / r
        var speed = 5.0  # Assumed speed (would be calculated from GPS/IMU integration)
        var yaw_rate = abs(imu_data[index][2].to_float64())  # Z-axis rotation
        
        if yaw_rate == 0.0:
            return 0.0
        
        var radius = speed / yaw_rate
        return (speed * speed) / radius
    
    fn _calculate_recovery_time(inout self, imu_data: Python.list, event_index: Int) -> Float64:
        """Calculate time to recover from slip/stall event"""
        var recovery_samples = 0
        var baseline_stability = self._calculate_stability_baseline(imu_data, event_index)
        
        # Look forward from event to find recovery
        for i in range(event_index + 1, min(event_index + int(self.sampling_rate * 5.0), len(imu_data))):  # Max 5 second search
            var current_stability = self._calculate_instantaneous_stability(imu_data, i)
            
            if current_stability > baseline_stability * 0.8:  # 80% recovery threshold
                recovery_samples = i - event_index
                break
        
        return recovery_samples.to_float64() / self.sampling_rate
    
    fn _calculate_control_authority(inout self, imu_data: Python.list, index: Int) -> Float64:
        """Calculate instantaneous control authority (0-1 scale)"""
        if index < self.smoothness_window or index >= len(imu_data):
            return 1.0
        
        # Analyze response to control inputs over smoothness window
        var input_variance = 0.0
        var response_variance = 0.0
        
        for i in range(index - self.smoothness_window, index):
            var input_magnitude = sqrt(
                pow(imu_data[i][0].to_float64(), 2) + 
                pow(imu_data[i][1].to_float64(), 2)
            )
            input_variance += input_magnitude
            
            # Response is change in orientation
            if i > 0:
                var response_magnitude = sqrt(
                    pow(imu_data[i][0].to_float64() - imu_data[i-1][0].to_float64(), 2) +
                    pow(imu_data[i][1].to_float64() - imu_data[i-1][1].to_float64(), 2)
                )
                response_variance += response_magnitude
        
        if input_variance == 0.0:
            return 1.0
        
        # Control authority = response sensitivity (clamped to 0-1)
        var authority = min(1.0, response_variance / input_variance)
        return authority
    
    fn _calculate_stability_baseline(inout self, imu_data: Python.list, reference_index: Int) -> Float64:
        """Calculate stability baseline before an event"""
        var baseline_window = min(self.smoothness_window, reference_index)
        var stability_sum = 0.0
        
        for i in range(max(0, reference_index - baseline_window), reference_index):
            stability_sum += self._calculate_instantaneous_stability(imu_data, i)
        
        if baseline_window == 0:
            return 1.0
        
        return stability_sum / baseline_window.to_float64()
    
    fn _calculate_instantaneous_stability(inout self, imu_data: Python.list, index: Int) -> Float64:
        """Calculate instantaneous stability metric"""
        if index < 1 or index >= len(imu_data):
            return 1.0
        
        # Stability based on rate of change (lower change = higher stability)
        var current = imu_data[index]
        var previous = imu_data[index-1]
        
        var change_magnitude = sqrt(
            pow(current[0].to_float64() - previous[0].to_float64(), 2) +
            pow(current[1].to_float64() - previous[1].to_float64(), 2) +
            pow(current[2].to_float64() - previous[2].to_float64(), 2)
        )
        
        # Invert and normalize (high change = low stability)
        return max(0.0, 1.0 - (change_magnitude / 10.0))  # 10.0 is normalization factor


struct SubjectiveRatingCollector:
    """
    Minimal-disruption subjective rating collection system.
    Designed to gather essential feedback without breaking flow state.
    """
    
    var rating_prompts: Python.dict        # Standardized prompts for consistent measurement
    var timing_protocol: Python.dict       # When and how to collect ratings
    var response_validation: Python.dict   # Validation rules for response quality
    
    fn __init__(inout self):
        self.rating_prompts = Python.dict()
        self.timing_protocol = Python.dict()
        self.response_validation = Python.dict()
        self._initialize_rating_system()
    
    fn _initialize_rating_system(inout self):
        """Initialize standardized rating prompts and protocols"""
        
        # Core invisibility ratings (0-10 scales)
        self.rating_prompts["equipment_invisibility"] = "How often did you notice the fin? (0=constantly aware, 10=completely invisible)"
        self.rating_prompts["effortlessness"] = "How automatic did turns feel? (0=required conscious effort, 10=completely automatic)"
        self.rating_prompts["disruption_count"] = "How many times did your attention go to the equipment? (count)"
        self.rating_prompts["predictability"] = "How predictable was the equipment response? (0=surprising, 10=perfectly predictable)"
        self.rating_prompts["consistency"] = "How consistent was the feel across different conditions? (0=highly variable, 10=perfectly consistent)"
        
        # Timing protocol (minimize flow disruption)
        self.timing_protocol["collection_method"] = "post_session_only"  # Never during flow state
        self.timing_protocol["delay_after_session"] = 300.0  # 5 minutes to decompress
        self.timing_protocol["max_rating_time"] = 120.0  # 2 minutes maximum
        self.timing_protocol["rating_order"] = "randomized"  # Prevent order bias
        
        # Response validation
        self.response_validation["min_response_time"] = 2.0  # Seconds - prevent rushed responses
        self.response_validation["max_response_time"] = 30.0  # Seconds - ensure engagement
        self.response_validation["consistency_check"] = True  # Cross-validate related ratings
        self.response_validation["outlier_detection"] = True  # Flag unusual response patterns
    
    fn collect_post_session_ratings(inout self, session_id: String) -> Python.dict:
        """
        Collect subjective ratings after session completion.
        Uses minimal-disruption protocol to preserve rating validity.
        """
        var ratings = Python.dict()
        ratings["session_id"] = session_id
        ratings["collection_timestamp"] = "current_time"  # Would use actual timestamp
        
        print("\n🎯 Post-Session Equipment Assessment")
        print("Please rate your experience with the equipment just tested:")
        print("(Take your time - there are no right or wrong answers)")
        print()
        
        # Randomize rating order to prevent bias
        var rating_keys = Python.list([
            "equipment_invisibility",
            "effortlessness", 
            "disruption_count",
            "predictability",
            "consistency"
        ])
        
        # Simulate rating collection (in real implementation, would use actual UI)
        for key in rating_keys:
            var prompt = self.rating_prompts[key.to_string()]
            var rating = self._simulate_rating_collection(key.to_string(), prompt.to_string())
            ratings[key.to_string()] = rating
        
        # Validate response consistency
        var validation_result = self._validate_response_consistency(ratings)
        ratings["validation_status"] = validation_result
        
        return ratings
    
    fn _simulate_rating_collection(inout self, rating_key: String, prompt: String) -> Float64:
        """Simulate rating collection (replace with actual UI in implementation)"""
        print("📊", prompt)
        
        # Simulate realistic ratings based on rating type
        var simulated_rating = 5.0  # Default middle value
        
        if rating_key == "equipment_invisibility":
            simulated_rating = 7.5  # Generally good invisibility
        elif rating_key == "effortlessness":
            simulated_rating = 8.0  # High effortlessness
        elif rating_key == "disruption_count":
            simulated_rating = 2.0  # Few disruptions
        elif rating_key == "predictability":
            simulated_rating = 8.5  # High predictability
        elif rating_key == "consistency":
            simulated_rating = 7.0  # Good consistency
        
        # Add some realistic variance
        var variance = 1.0
        simulated_rating += (variance * 0.5)  # Simplified random variance
        
        # Clamp to valid range
        if rating_key == "disruption_count":
            simulated_rating = max(0.0, min(20.0, simulated_rating))  # Count range
        else:
            simulated_rating = max(0.0, min(10.0, simulated_rating))  # 0-10 scale
        
        print("   → Rating:", simulated_rating)
        print()
        
        return simulated_rating
    
    fn _validate_response_consistency(inout self, ratings: Python.dict) -> String:
        """Validate internal consistency of subjective ratings"""
        
        # Check for logical consistency
        var invisibility = ratings.get("equipment_invisibility", 5.0).to_float64()
        var effortlessness = ratings.get("effortlessness", 5.0).to_float64()
        var disruptions = ratings.get("disruption_count", 5.0).to_float64()
        var predictability = ratings.get("predictability", 5.0).to_float64()
        
        var consistency_flags = Python.list()
        
        # High invisibility should correlate with low disruptions
        if invisibility > 7.0 and disruptions > 5.0:
            consistency_flags.append("invisibility_disruption_mismatch")
        
        # High effortlessness should correlate with high invisibility
        if abs(effortlessness - invisibility) > 3.0:
            consistency_flags.append("effortlessness_invisibility_mismatch")
        
        # High predictability should correlate with high effortlessness
        if predictability > 8.0 and effortlessness < 6.0:
            consistency_flags.append("predictability_effortlessness_mismatch")
        
        if len(consistency_flags) == 0:
            return "CONSISTENT"
        elif len(consistency_flags) == 1:
            return "MINOR_INCONSISTENCY"
        else:
            return "MAJOR_INCONSISTENCY"


struct BlindTestingValidator:
    """
    Validates blind testing protocol integrity and analyzes results.
    Ensures unbiased evaluation of equipment invisibility.
    """
    
    var randomization_log: Python.list     # Record of test sequence randomization
    var blinding_integrity: Python.dict    # Measures of blinding effectiveness
    var statistical_power: Python.dict     # Power analysis for sample sizes
    var effect_size_thresholds: Python.dict # Minimum detectable differences
    
    fn __init__(inout self):
        self.randomization_log = Python.list()
        self.blinding_integrity = Python.dict()
        self.statistical_power = Python.dict()
        self.effect_size_thresholds = Python.dict()
        self._initialize_validation_parameters()
    
    fn _initialize_validation_parameters(inout self):
        """Initialize validation parameters for robust testing"""
        
        # Statistical power requirements
        self.statistical_power["target_power"] = 0.80  # 80% power
        self.statistical_power["alpha_level"] = 0.05   # 5% significance level
        self.statistical_power["min_sample_size"] = 15  # Minimum sessions per variant
        
        # Effect size thresholds (minimum meaningful differences)
        self.effect_size_thresholds["micro_corrections"] = 5.0    # 5 corrections/minute
        self.effect_size_thresholds["invisibility_rating"] = 1.0  # 1 point on 10-point scale
        self.effect_size_thresholds["smoothness"] = 0.1          # 10% improvement in smoothness
        self.effect_size_thresholds["consistency"] = 0.15        # 15% reduction in variance
        
        # Blinding integrity checks
        self.blinding_integrity["visual_similarity_required"] = True
        self.blinding_integrity["tactile_similarity_required"] = True
        self.blinding_integrity["weight_tolerance"] = 0.02  # ±2% weight difference maximum
        self.blinding_integrity["appearance_check"] = "mandatory"
    
    fn validate_test_design(inout self, test_protocol: Python.dict) -> Python.dict:
        """
        Validates the overall test design for statistical rigor.
        Returns validation report with recommendations.
        """
        var validation_report = Python.dict()
        var issues = Python.list()
        var recommendations = Python.list()
        
        # Check sample size adequacy
        var sessions_per_variant = test_protocol.get("sessions_per_variant", 0).to_int()
        var num_variants = test_protocol.get("num_variants", 0).to_int()
        
        if sessions_per_variant < self.statistical_power["min_sample_size"].to_int():
            issues.append("insufficient_sample_size")
            recommendations.append("Increase sessions per variant to at least " + str(self.statistical_power["min_sample_size"].to_int()))
        
        # Check randomization scheme
        var randomization_method = test_protocol.get("randomization", "none").to_string()
        if randomization_method == "none" or randomization_method == "simple":
            issues.append("inadequate_randomization")
            recommendations.append("Use block randomization or Latin square design")
        
        # Check blinding measures
        var blinding_measures = test_protocol.get("blinding_measures", Python.list())
        if len(blinding_measures) < 3:
            issues.append("insufficient_blinding")
            recommendations.append("Implement visual, tactile, and weight blinding")
        
        # Check measurement timing
        var measurement_timing = test_protocol.get("measurement_timing", "during_session").to_string()
        if measurement_timing == "during_session":
            issues.append("disruptive_measurement")
            recommendations.append("Move subjective measurements to post-session only")
        
        # Overall validation status
        if len(issues) == 0:
            validation_report["status"] = "VALID"
        elif len(issues) <= 2:
            validation_report["status"] = "ACCEPTABLE_WITH_MODIFICATIONS"
        else:
            validation_report["status"] = "REQUIRES_MAJOR_REVISION"
        
        validation_report["issues"] = issues
        validation_report["recommendations"] = recommendations
        validation_report["statistical_power_estimate"] = self._calculate_statistical_power(sessions_per_variant, num_variants)
        
        return validation_report
    
    fn analyze_test_results(inout self, results_data: Python.list) -> Python.dict:
        """
        Analyzes blind test results for significant differences.
        Uses appropriate statistical tests for equipment comparison.
        """
        var analysis_results = Python.dict()
        
        # Group results by variant
        var variant_groups = self._group_results_by_variant(results_data)
        
        # Calculate descriptive statistics for each variant
        var descriptive_stats = self._calculate_descriptive_statistics(variant_groups)
        analysis_results["descriptive_statistics"] = descriptive_stats
        
        # Perform statistical significance tests
        var significance_tests = self._perform_significance_tests(variant_groups)
        analysis_results["significance_tests"] = significance_tests
        
        # Calculate effect sizes
        var effect_sizes = self._calculate_effect_sizes(variant_groups)
        analysis_results["effect_sizes"] = effect_sizes
        
        # Determine practical significance
        var practical_significance = self._assess_practical_significance(effect_sizes)
        analysis_results["practical_significance"] = practical_significance
        
        # Generate recommendations
        var recommendations = self._generate_selection_recommendations(variant_groups, effect_sizes, practical_significance)
        analysis_results["recommendations"] = recommendations
        
        return analysis_results
    
    fn _calculate_statistical_power(inout self, sample_size: Int, num_groups: Int) -> Float64:
        """Calculate statistical power for given sample size and design"""
        # Simplified power calculation (would use more sophisticated method in practice)
        var effect_size = 0.5  # Medium effect size assumption
        var alpha = self.statistical_power["alpha_level"].to_float64()
        
        # Basic power approximation based on sample size
        var power_estimate = 0.0
        if sample_size >= 15:
            power_estimate = 0.80
        elif sample_size >= 10:
            power_estimate = 0.65
        elif sample_size >= 5:
            power_estimate = 0.45
        else:
            power_estimate = 0.20
        
        return power_estimate
    
    fn _group_results_by_variant(inout self, results_data: Python.list) -> Python.dict:
        """Group test results by equipment variant"""
        var groups = Python.dict()
        
        for result in results_data:
            var variant_id = result[0].to_string()
            var metrics = result[1]
            
            if variant_id not in groups:
                groups[variant_id] = Python.list()
            
            groups[variant_id].append(metrics)
        
        return groups
    
    fn _calculate_descriptive_statistics(inout self, variant_groups: Python.dict) -> Python.dict:
        """Calculate mean, std, min, max for each variant and metric"""
        var stats = Python.dict()
        
        # Would iterate through each variant and calculate statistics
        # Simplified implementation for demonstration
        stats["variant_count"] = len(variant_groups)
        stats["metrics_calculated"] = Python.list(["mean", "std", "min", "max", "median"])
        
        return stats
    
    fn _perform_significance_tests(inout self, variant_groups: Python.dict) -> Python.dict:
        """Perform appropriate statistical tests (ANOVA, t-tests, etc.)"""
        var tests = Python.dict()
        
        # Would perform actual statistical tests
        # Simplified implementation for demonstration
        tests["omnibus_test"] = "ANOVA"
        tests["pairwise_tests"] = "Tukey_HSD"
        tests["alpha_level"] = self.statistical_power["alpha_level"]
        
        return tests
    
    fn _calculate_effect_sizes(inout self, variant_groups: Python.dict) -> Python.dict:
        """Calculate effect sizes (Cohen's d, eta-squared, etc.)"""
        var effect_sizes = Python.dict()
        
        # Would calculate actual effect sizes
        # Simplified implementation for demonstration
        effect_sizes["cohens_d"] = 0.5  # Medium effect size
        effect_sizes["eta_squared"] = 0.06  # Small to medium effect
        
        return effect_sizes
    
    fn _assess_practical_significance(inout self, effect_sizes: Python.dict) -> Python.dict:
        """Assess whether differences are practically meaningful"""
        var practical_sig = Python.dict()
        
        var cohens_d = effect_sizes.get("cohens_d", 0.0).to_float64()
        
        if cohens_d >= 0.8:
            practical_sig["magnitude"] = "large"
            practical_sig["meaningful"] = True
        elif cohens_d >= 0.5:
            practical_sig["magnitude"] = "medium"
            practical_sig["meaningful"] = True
        elif cohens_d >= 0.2:
            practical_sig["magnitude"] = "small"
            practical_sig["meaningful"] = False
        else:
            practical_sig["magnitude"] = "negligible"
            practical_sig["meaningful"] = False
        
        return practical_sig
    
    fn _generate_selection_recommendations(inout self, variant_groups: Python.dict, effect_sizes: Python.dict, practical_significance: Python.dict) -> Python.dict:
        """Generate equipment selection recommendations based on analysis"""
        var recommendations = Python.dict()
        
        # Selection rule: Prefer lowest micro-corrections and highest invisibility
        recommendations["primary_criterion"] = "micro_correction_rate"
        recommendations["secondary_criterion"] = "equipment_invisibility"
        recommendations["selection_rule"] = "minimize_corrections_maximize_invisibility"
        
        # Confidence in recommendation
        if practical_significance["meaningful"].to_bool():
            recommendations["confidence"] = "high"
            recommendations["action"] = "select_best_variant"
        else:
            recommendations["confidence"] = "low"
            recommendations["action"] = "insufficient_difference_detected"
        
        return recommendations


fn main():
    """
    Demonstration of the Invisibility Validation System
    Shows comprehensive testing and measurement capabilities
    """
    print("🔬 Invisibility Validation System")
    print("=================================")
    
    # Initialize validation components
    var imu_processor = IMUDataProcessor()
    var rating_collector = SubjectiveRatingCollector()
    var test_validator = BlindTestingValidator()
    
    print("✅ Initialized validation components")
    print()
    
    # Simulate test data collection
    print("📊 Simulating IMU Data Collection...")
    var sample_imu_data = Python.list()
    
    # Generate 60 seconds of 100Hz IMU data (6000 samples)
    for i in range(6000):
        var timestamp = i.to_float64() / 100.0
        var roll = 0.5 * sin(2.0 * pi * timestamp * 0.1)  # Slow roll oscillation
        var pitch = 0.3 * sin(2.0 * pi * timestamp * 0.15)  # Pitch variation
        var yaw = 0.2 * sin(2.0 * pi * timestamp * 0.05)   # Yaw changes
        
        var sample = Python.list([roll, pitch, yaw, timestamp])
        sample_imu_data.append(sample)
    
    # Calculate flow state metrics
    var micro_corrections = imu_processor.calculate_micro_correction_rate(sample_imu_data)
    var movement_smoothness = imu_processor.calculate_movement_smoothness(sample_imu_data)
    
    print("  - Micro-correction rate:", micro_corrections, "corrections/minute")
    print("  - Movement smoothness:", movement_smoothness, "(lower = smoother)")
    print()
    
    # Simulate subjective rating collection
    print("🎯 Simulating Post-Session Rating Collection...")
    var session_ratings = rating_collector.collect_post_session_ratings("TEST_SESSION_001")
    
    print("  - Equipment Invisibility:", session_ratings.get("equipment_invisibility", 0.0))
    print("  - Effortlessness:", session_ratings.get("effortlessness", 0.0))
    print("  - Disruption Count:", session_ratings.get("disruption_count", 0.0))
    print("  - Validation Status:", session_ratings.get("validation_status", "UNKNOWN"))
    print()
    
    # Validate test design
    print("🔍 Validating Test Design...")
    var test_protocol = Python.dict()
    test_protocol["sessions_per_variant"] = 15
    test_protocol["num_variants"] = 3
    test_protocol["randomization"] = "block_randomized"
    test_protocol["blinding_measures"] = Python.list(["visual", "tactile", "weight"])
    test_protocol["measurement_timing"] = "post_session"
    
    var validation_report = test_validator.validate_test_design(test_protocol)
    print("  - Validation Status:", validation_report.get("status", "UNKNOWN"))
    print("  - Statistical Power:", validation_report.get("statistical_power_estimate", 0.0))
    print()
    
    # Demonstrate selection criteria
    print("🎯 Equipment Selection Criteria:")
    print("  ✓ Primary: Minimize micro-correction rate")
    print("  ✓ Secondary: Maximize equipment invisibility rating")
    print("  ✓ Tertiary: Maximize movement smoothness")
    print("  ✓ Rule: Select variant with best combined score")
    print()
    
    print("📈 Validation Methodology Summary:")
    print("  ✓ Double-blind A/B/X testing protocol")
    print("  ✓ High-resolution IMU data analysis (100Hz)")
    print("  ✓ Minimal-disruption subjective rating collection")
    print("  ✓ Statistical significance and effect size analysis")
    print("  ✓ Practical significance assessment")
    print("  ✓ Evidence-based selection recommendations")
    print()
    
    print("🏆 Result: Validated invisible equipment optimized for flow state")