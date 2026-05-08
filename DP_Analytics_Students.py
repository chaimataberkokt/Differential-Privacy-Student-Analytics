import numpy as np
import pandas as pd


class DP_Analytics_Students:
    """
    A production-ready differential privacy analytics system for student data.

    Computes statistics on student performance while preserving privacy using
    Laplace and Gaussian mechanisms.

    Privacy budget accounting
    -------------------------
    When ``equal_split=True`` (the default), the total epsilon supplied to
    ``dp_queries()`` is divided equally across all ``NUM_QUERIES`` queries
    **before** being passed to the noise mechanism::

        eps_per_query = epsilon_total / NUM_QUERIES

    All privacy-level assessments in the dashboard are therefore based on
    ``eps_per_query``, not on ``epsilon_total``.  This is the value that
    controls the actual noise scale.
    """

    # Number of independent statistics computed by dp_queries().
    # Changing this constant automatically updates both the budget split
    # and the eps_per_query value exposed in the result dictionary.
    NUM_QUERIES: int = 5
    
    def __init__(self, csv_path, pass_threshold=10):
        """
        Initialize the analytics system by loading and preprocessing data.
        
        Args:
            csv_path (str): Path to the CSV file containing student data
            pass_threshold (float): Threshold for pass/fail classification
        """
        self.df = self._load_and_preprocess(csv_path, pass_threshold)
        self.pass_threshold = pass_threshold
        self.N = len(self.df)
        self._compute_ranges()
        self._compute_true_stats()
        self._compute_sensitivities()
    
    
   
    # DATA LOADING & PREPROCESSING

    
    def _load_and_preprocess(self, csv_path, pass_threshold):
        """Load CSV and standardize column names and create derived features."""
        df = pd.read_csv(csv_path)
        
        # Standardize column names
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # Create quiz average
        df["quiz_avg"] = df[["quiz_1", "quiz_2", "quiz_3"]].mean(axis=1)
        
        # Create passed column
        df["passed"] = (df["course_mark"] >= pass_threshold).astype(int)
        
        return df
    
    
    def _compute_ranges(self):
        """Compute min, max, and range for all key features."""
        self.final_min = float(self.df["final_mark"].min())
        self.final_max = float(self.df["final_mark"].max())
        self.final_range = self.final_max - self.final_min
        
        self.part_min = float(self.df["participation_avg"].min())
        self.part_max = float(self.df["participation_avg"].max())
        self.part_range = self.part_max - self.part_min
        
        self.quiz_min = float(self.df["quiz_avg"].min())
        self.quiz_max = float(self.df["quiz_avg"].max())
        self.quiz_range = self.quiz_max - self.quiz_min
    
    
    # TRUE STATISTICS COMPUTATION
    
    def _compute_true_stats(self):
        """Compute exact non-private statistics."""
        self.true_stats = {
            "mean_final_mark": float(self.df["final_mark"].mean()),
            "mean_participation": float(self.df["participation_avg"].mean()),
            "mean_quiz_avg": float(self.df["quiz_avg"].mean()),
            "count": float(self.N),
            "pass_rate": float(self.df["passed"].mean()),
        }
    
    

    # SENSITIVITY FUNCTIONS
 
    
    def _compute_sensitivities(self):
        """Compute sensitivity for each query type."""
        self.sensitivities = {
            "count": self._sensitivity_count(),
            "mean_final_mark": self._sensitivity_mean(self.N, self.final_range),
            "mean_participation": self._sensitivity_mean(self.N, self.part_range),
            "mean_quiz_avg": self._sensitivity_mean(self.N, self.quiz_range),
            "pass_rate": self._sensitivity_pass_rate(self.N),
        }
    
    
    @staticmethod
    def _sensitivity_count():
        """Sensitivity for count queries: Δ = 1"""
        return 1.0
    
    
    @staticmethod
    def _sensitivity_mean(n, value_range):
        """Sensitivity for mean queries: Δ = (max - min) / n"""
        return value_range / n
    
    
    @staticmethod
    def _sensitivity_pass_rate(n):
        """Sensitivity for pass rate (binary mean): Δ = 1 / n"""
        return 1.0 / n
    
    
    # DIFFERENTIAL PRIVACY MECHANISMS
   
    
    @staticmethod
    def _laplace_mechanism(value, sensitivity, epsilon):
        """
        Laplace mechanism for ε-DP.
        
        Adds noise drawn from Laplace(0, sensitivity/epsilon)
        
        Args:
            value: The true statistic
            sensitivity: Sensitivity of the query
            epsilon: Privacy parameter
            
        Returns:
            Noisy value
        """
        if epsilon <= 0:
            raise ValueError("epsilon must be > 0")
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale)
        return value + noise
    
    
    @staticmethod
    def _gaussian_mechanism(value, sensitivity, epsilon, delta=1e-5):
        """
        Gaussian mechanism for (ε, δ)-DP.
        
        Adds noise drawn from N(0, sigma^2) where
        sigma = sqrt(2 * log(1.25/delta)) * sensitivity / epsilon
        
        Args:
            value: The true statistic
            sensitivity: Sensitivity of the query
            epsilon: Privacy parameter
            delta: Failure probability (default 1e-5)
            
        Returns:
            Noisy value
        """
        if epsilon <= 0 or delta <= 0:
            raise ValueError("epsilon and delta must be > 0")
        sigma = np.sqrt(2 * np.log(1.25 / delta)) * sensitivity / epsilon
        noise = np.random.normal(0, sigma)
        return value + noise
    
    
    @staticmethod
    def _apply_dp(true_val, sensitivity, epsilon, mechanism="laplace"):
        """
        Apply differential privacy mechanism to a value.
        
        Args:
            true_val: The true statistic
            sensitivity: Sensitivity of the query
            epsilon: Privacy parameter
            mechanism: "laplace" or "gaussian"
            
        Returns:
            Differentially private value
        """
        if mechanism == "laplace":
            return DP_Analytics_Students._laplace_mechanism(true_val, sensitivity, epsilon)
        elif mechanism == "gaussian":
            return DP_Analytics_Students._gaussian_mechanism(true_val, sensitivity, epsilon)
        else:
            raise ValueError(f"Unknown mechanism: {mechanism}")
    
    
    
    # DP QUERY FUNCTIONS
   
    
    def query_mean_final_mark(self, epsilon, mechanism="laplace"):
        """Return DP mean of final marks."""
        val = self.df["final_mark"].mean()
        sens = self.sensitivities["mean_final_mark"]
        return self._apply_dp(val, sens, epsilon, mechanism)
    
    
    def query_mean_participation(self, epsilon, mechanism="laplace"):
        """Return DP mean of participation."""
        val = self.df["participation_avg"].mean()
        sens = self.sensitivities["mean_participation"]
        return self._apply_dp(val, sens, epsilon, mechanism)
    
    
    def query_mean_quiz_avg(self, epsilon, mechanism="gaussian"):
        """Return DP mean of quiz average."""
        val = self.df["quiz_avg"].mean()
        sens = self.sensitivities["mean_quiz_avg"]
        return self._apply_dp(val, sens, epsilon, mechanism)
    
    
    def query_count(self, epsilon, mechanism="laplace"):
        """Return DP count of students."""
        val = float(self.N)
        sens = self.sensitivities["count"]
        return self._apply_dp(val, sens, epsilon, mechanism)
    
    
    def query_pass_rate(self, epsilon, mechanism="laplace"):
        """Return DP pass rate."""
        val = self.df["passed"].mean()
        sens = self.sensitivities["pass_rate"]
        return self._apply_dp(val, sens, epsilon, mechanism)
    
    
    # CENTRAL DP QUERY ENGINE
    
    
    def dp_queries(self, epsilon, mechanism="laplace", equal_split=True):
        """
        Compute all DP statistics in one query.

        When ``equal_split=True`` the total privacy budget is divided evenly
        across all ``NUM_QUERIES`` queries (sequential composition theorem).
        The effective per-query epsilon is stored in the returned dictionary
        under the key ``"eps_per_query"`` so that callers — such as the
        Streamlit dashboard — can display the value that was *actually* used
        by the noise mechanism, rather than the potentially misleading total.

        Args:
            epsilon (float): Total privacy budget (ε_total)
            mechanism (str): ``"laplace"`` for strict ε-DP or
                             ``"gaussian"`` for approximate (ε, δ)-DP.
            equal_split (bool): If True, split epsilon equally among queries
                                 using the sequential composition theorem.

        Returns:
            dict: Keys:
                - ``epsilon``       – total budget supplied by the caller
                - ``eps_per_query`` – per-query budget actually used for noise
                - ``num_queries``   – number of queries (= NUM_QUERIES)
                - ``equal_split``   – whether budget was split
                - ``mechanism``     – noise mechanism used
                - ``true_stats``    – exact statistics (no noise)
                - ``sensitivities`` – sensitivity of each query
                - ``noisy_stats``   – differentially private statistics
        """
        # --- Budget allocation -------------------------------------------
        # Use the class-level constant so there is a single source of truth.
        if equal_split:
            
            eps_per_query = epsilon / self.NUM_QUERIES
        else:
            eps_per_query = epsilon

        result = {
            "epsilon": epsilon,
            # Expose the effective per-query epsilon so the UI can use it
            # for privacy-level assessments instead of the total budget.
            "eps_per_query": eps_per_query,
            "num_queries": self.NUM_QUERIES,
            "equal_split": equal_split,
            "mechanism": mechanism,
            "true_stats": self.true_stats.copy(),
            "sensitivities": self.sensitivities.copy(),
            "noisy_stats": {
                "mean_final_mark":   self.query_mean_final_mark(eps_per_query, mechanism),
                "mean_participation": self.query_mean_participation(eps_per_query, mechanism),
                "mean_quiz_avg":     self.query_mean_quiz_avg(eps_per_query, mechanism),
                "count":             self.query_count(eps_per_query, mechanism),
                "pass_rate":         self.query_pass_rate(eps_per_query, mechanism),
            },
        }

        return result
    
   
    # UTILITY EVALUATION METRICS
  
    
    @staticmethod
    def mae(true, pred):
        """Mean Absolute Error"""
        return abs(true - pred)
    
    
    @staticmethod
    def rmse(true, pred):
        """Root Mean Squared Error"""
        return ((true - pred) ** 2) ** 0.5
    
    
    @staticmethod
    def relative_error(true, pred):
        """Relative Error (%)"""
        if true == 0:
            return 0
        return abs(true - pred) / abs(true) * 100
    
    
    def evaluate_utility(self, results):
        """
        Evaluate utility of DP results.
        
        Args:
            results (dict): Output from dp_queries()
            
        Returns:
            dict: Contains MAE, RMSE, and relative error for each query
        """
        true_vals = results["true_stats"]
        noisy_vals = results["noisy_stats"]
        
        evaluation = {}
        for key in true_vals.keys():
            true = true_vals[key]
            noisy = noisy_vals[key]
            
            evaluation[key] = {
                "MAE": self.mae(true, noisy),
                "RMSE": self.rmse(true, noisy),
                "Relative_Error_%": self.relative_error(true, noisy),
            }
        
        return evaluation
    
    
   
    # PRIVACY BUDGET MANAGEMENT
    
    
    def get_dataset_profile(self):
        """
        Return dataset profiling information.
        
        Returns:
            dict: Contains dataset characteristics
        """
        return {
            "students_count": self.N,
            "final_mark_range": (self.final_min, self.final_max),
            "participation_range": (self.part_min, self.part_max),
            "quiz_avg_range": (self.quiz_min, self.quiz_max),
            "pass_threshold": self.pass_threshold,
            "pass_rate": self.true_stats["pass_rate"],
            "true_stats": self.true_stats,
            "sensitivities": self.sensitivities,
        }
    
    
    def get_data(self):
        """Return the preprocessed dataframe."""
        return self.df.copy()


    # OPTIMAL EPSILON SEARCH


    def find_optimal_epsilon(
        self,
        mechanism="laplace",
        metric="mean_final_mark",
        target_relative_error=5.0,
        trials_per_eps=20,
        coarse_range=None,
        fine_steps=20,
    ):
        """
        Two-phase grid search to find the optimal epsilon.

        Phase 1 (Coarse): Sweep a wide range of epsilon values and compute
        average relative error across multiple trials for each.

        Phase 2 (Fine): Narrow the search around the elbow region found in
        Phase 1 and refine with smaller steps.

        The "optimal" epsilon is defined as the elbow point — the value where
        further increases in epsilon yield diminishing accuracy gains.  This is
        detected geometrically: the point with maximum perpendicular distance
        from the chord connecting the first and last points of the normalised
        error curve.

        Args:
            mechanism (str): ``"laplace"`` or ``"gaussian"``
            metric (str): Which statistic to optimise for
            target_relative_error (float): Desired relative error threshold (%)
            trials_per_eps (int): Number of trials per epsilon candidate
            coarse_range (list|None): Custom coarse epsilon grid; if None, uses
                a sensible default ``[0.01 .. 2.0]``
            fine_steps (int): Number of steps in the fine-grained phase

        Returns:
            dict:
                - ``optimal_epsilon``      – recommended epsilon (elbow point)
                - ``threshold_epsilon``     – smallest epsilon achieving the
                  target relative error (or None if not achievable)
                - ``target_relative_error`` – the target that was requested
                - ``sweep_data``           – list of dicts with ``epsilon``,
                  ``avg_relative_error``, ``avg_absolute_error``,
                  ``std_relative_error`` for every tested value
                - ``phase``                – ``"coarse+fine"``
        """
        if coarse_range is None:
            coarse_range = [
                0.01, 0.02, 0.05, 0.08,
                0.10, 0.15, 0.20, 0.30,
                0.40, 0.50, 0.60, 0.80,
                1.00, 1.25, 1.50, 2.00,
            ]

        # ---------- helper: evaluate one epsilon value ----------
        def _evaluate(eps):
            rel_errors, abs_errors = [], []
            for _ in range(trials_per_eps):
                res = self.dp_queries(epsilon=eps, mechanism=mechanism,
                                      equal_split=False)
                true_val  = res["true_stats"][metric]
                noisy_val = res["noisy_stats"][metric]
                ae = abs(true_val - noisy_val)
                re = (ae / abs(true_val) * 100) if true_val != 0 else 0
                abs_errors.append(ae)
                rel_errors.append(re)
            return {
                "epsilon":            eps,
                "avg_relative_error": float(np.mean(rel_errors)),
                "std_relative_error": float(np.std(rel_errors)),
                "avg_absolute_error": float(np.mean(abs_errors)),
            }

        # ---------- Phase 1: coarse sweep ----------
        sweep = [_evaluate(eps) for eps in coarse_range]

        # ---------- Elbow detection (max distance from chord) ----------
        def _find_elbow(data):
            """Return the index of the elbow point."""
            eps_vals = np.array([d["epsilon"] for d in data])
            err_vals = np.array([d["avg_relative_error"] for d in data])

            # normalise to [0,1]
            eps_n = (eps_vals - eps_vals.min()) / (eps_vals.max() - eps_vals.min() + 1e-12)
            err_n = (err_vals - err_vals.min()) / (err_vals.max() - err_vals.min() + 1e-12)

            # chord from first to last point
            p1 = np.array([eps_n[0], err_n[0]])
            p2 = np.array([eps_n[-1], err_n[-1]])
            line_vec = p2 - p1
            line_len = np.linalg.norm(line_vec)
            if line_len < 1e-12:
                return len(data) // 2

            # perpendicular distance of each point from the chord
            distances = []
            for i in range(len(data)):
                pt = np.array([eps_n[i], err_n[i]])
                dist = abs(np.cross(line_vec, p1 - pt)) / line_len
                distances.append(dist)

            return int(np.argmax(distances))

        elbow_idx = _find_elbow(sweep)
        elbow_eps = sweep[elbow_idx]["epsilon"]

        # ---------- Phase 2: fine sweep around elbow ----------
        low  = sweep[max(0, elbow_idx - 1)]["epsilon"]
        high = sweep[min(len(sweep) - 1, elbow_idx + 1)]["epsilon"]
        fine_range = np.linspace(low, high, fine_steps).tolist()

        fine_sweep = [_evaluate(eps) for eps in fine_range]
        all_data   = sorted(sweep + fine_sweep, key=lambda d: d["epsilon"])

        # re-detect elbow on combined data
        elbow_idx_final = _find_elbow(all_data)
        optimal_eps = all_data[elbow_idx_final]["epsilon"]

        # ---------- Threshold epsilon ----------
        threshold_eps = None
        for d in all_data:
            if d["avg_relative_error"] <= target_relative_error:
                threshold_eps = d["epsilon"]
                break

        return {
            "optimal_epsilon":      round(optimal_eps, 4),
            "threshold_epsilon":    round(threshold_eps, 4) if threshold_eps else None,
            "target_relative_error": target_relative_error,
            "sweep_data":           all_data,
            "phase":                "coarse+fine",
        }


class PrivacyBudget:
    """Manages privacy budget allocation across multiple queries."""
    
    def __init__(self, epsilon_total):
        """
        Initialize privacy budget.
        
        Args:
            epsilon_total (float): Total privacy budget
        """
        self.epsilon_total = epsilon_total
        self.epsilon_spent = 0.0
    
    
    def spend(self, epsilon):
        """
        Allocate epsilon from budget.
        
        Args:
            epsilon (float): Amount to spend
            
        Returns:
            float: The allocated epsilon
            
        Raises:
            ValueError: If budget exceeded
        """
        if self.epsilon_spent + epsilon > self.epsilon_total:
            raise ValueError("Privacy budget exceeded!")
        self.epsilon_spent += epsilon
        return epsilon
    
    
    def remaining(self):
        """Return remaining budget."""
        return self.epsilon_total - self.epsilon_spent
    
    
    def summary(self):
        """Return budget summary as dictionary."""
        return {
            "total_budget": self.epsilon_total,
            "spent": self.epsilon_spent,
            "remaining": self.remaining()
        }


# Example usage
if __name__ == "__main__":
    # Initialize the system
    analytics = DP_Analytics_Students("students.csv", pass_threshold=10)
    
    # Get dataset profile
    profile = analytics.get_dataset_profile()
    
    # Run DP queries with epsilon=0.3
    results = analytics.dp_queries(epsilon=0.3, mechanism="laplace", equal_split=True)
    
    # Evaluate utility
    utility = analytics.evaluate_utility(results)
    
    print("DP Analytics System Initialized")
    print(f"Dataset Profile: {profile}")
    print(f"Query Results: {results}")
    print(f"Utility Evaluation: {utility}")
