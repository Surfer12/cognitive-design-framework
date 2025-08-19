#!/usr/bin/env python3
"""
Latent Space Visualization for Medical AI Ensemble Systems
Applies t-SNE and PCA to visualize patient parameter spaces and model learning

Mathematical Framework:
1. Patient latent representations: z_i = E(x_i) ∈ ℝ^d
2. PCA projection: z_i^(PCA) = V_k^T · (z_i - z̄) ∈ ℝ^k  
3. t-SNE embedding: minimize KL(P||Q) where P is high-D, Q is low-D similarities
4. Visualization of: clusters, trajectories, optimization paths, unexplored regions

Applications:
- Patient similarity clustering
- Treatment optimization paths
- Model ensemble behavior visualization
- Clinical decision boundary mapping
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns

@dataclass
class PatientLatentPoint:
    """Patient representation in latent space."""
    patient_id: str
    latent_vector: np.ndarray  # z_i ∈ ℝ^d
    clinical_features: Dict[str, float]
    predicted_dose: float
    actual_outcome: Optional[float]
    risk_category: str  # 'low', 'medium', 'high'
    treatment_response: str  # 'good', 'poor', 'adverse'

class MedicalLatentSpaceAnalyzer:
    """
    Latent space analysis for medical AI ensemble systems.
    
    Mathematical operations:
    1. Latent encoding: z = E(patient_features)
    2. Dimensionality reduction: PCA/t-SNE
    3. Cluster analysis: patient similarity groups
    4. Trajectory analysis: treatment optimization paths
    """
    
    def __init__(self):
        self.patients: List[PatientLatentPoint] = []
        self.latent_matrix: Optional[np.ndarray] = None  # Z ∈ ℝ^{n×d}
        self.pca_embeddings: Optional[np.ndarray] = None
        self.tsne_embeddings: Optional[np.ndarray] = None
        self.pca_model: Optional[PCA] = None
        self.scaler: Optional[StandardScaler] = None
        
    def add_patient(self, patient: PatientLatentPoint):
        """Add patient to latent space analysis."""
        self.patients.append(patient)
        
    def encode_patients_to_latent(self, ensemble_model=None) -> np.ndarray:
        """
        Encode patients to latent space representations.
        
        Mathematical formulation:
        z_i = E(x_i) where x_i are patient features
        
        Returns: Z ∈ ℝ^{n×d} latent matrix
        """
        
        if not self.patients:
            raise ValueError("No patients added for analysis")
        
        # Extract patient features for encoding
        patient_features = []
        for patient in self.patients:
            # Combine clinical features into feature vector
            features = [
                patient.clinical_features.get('age', 50) / 100.0,
                patient.clinical_features.get('weight', 70) / 100.0,
                1.0 if patient.clinical_features.get('sex', 'M') == 'M' else 0.0,
                patient.clinical_features.get('creatinine', 1.0) / 3.0,
                patient.clinical_features.get('cyp3a4_score', 1.0),
                patient.clinical_features.get('adherence', 1.0),
                patient.predicted_dose / 500.0,  # Normalized dose
                1.0 if patient.risk_category == 'high' else 0.5 if patient.risk_category == 'medium' else 0.0
            ]
            patient_features.append(features)
        
        # Convert to numpy array
        feature_matrix = np.array(patient_features)
        
        # Simple latent encoding (in practice, would use trained encoder)
        # For demonstration, we'll use a linear transformation + nonlinearity
        np.random.seed(42)
        W_encoder = np.random.normal(0, 0.1, (feature_matrix.shape[1], 16))  # Encode to 16D
        
        # z_i = tanh(W * x_i + b) - simple encoder
        latent_vectors = np.tanh(np.dot(feature_matrix, W_encoder))
        
        # Add some patient-specific variation
        for i, patient in enumerate(self.patients):
            if patient.treatment_response == 'poor':
                latent_vectors[i] += np.random.normal(0, 0.1, latent_vectors.shape[1])
            elif patient.treatment_response == 'adverse':
                latent_vectors[i] += np.random.normal(0, 0.2, latent_vectors.shape[1])
        
        self.latent_matrix = latent_vectors
        return latent_vectors
    
    def compute_pca_embedding(self, n_components: int = 2) -> np.ndarray:
        """
        Compute PCA embedding of latent space.
        
        Mathematical formulation:
        1. Center data: z̄ = (1/n) Σ z_i, z̃_i = z_i - z̄
        2. Covariance: Σ = (1/n) Σ z̃_i z̃_i^T
        3. Eigendecomposition: Σ = V Λ V^T
        4. Project: z_i^(PCA) = V_k^T · z̃_i
        """
        
        if self.latent_matrix is None:
            self.encode_patients_to_latent()
        
        # Standardize the data
        self.scaler = StandardScaler()
        latent_scaled = self.scaler.fit_transform(self.latent_matrix)
        
        # Apply PCA
        self.pca_model = PCA(n_components=n_components)
        self.pca_embeddings = self.pca_model.fit_transform(latent_scaled)
        
        return self.pca_embeddings
    
    def compute_tsne_embedding(self, n_components: int = 2, perplexity: float = 30.0) -> np.ndarray:
        """
        Compute t-SNE embedding of latent space.
        
        Mathematical formulation:
        1. High-D similarities: p_ij = exp(-||z_i - z_j||²/2σ²) / Σ_kl exp(-||z_k - z_l||²/2σ²)
        2. Low-D similarities: q_ij = (1 + ||y_i - y_j||²)^(-1) / Σ_kl (1 + ||y_k - y_l||²)^(-1)
        3. Minimize KL divergence: L = Σ_ij p_ij log(p_ij/q_ij)
        """
        
        if self.latent_matrix is None:
            self.encode_patients_to_latent()
        
        # Standardize the data
        if self.scaler is None:
            self.scaler = StandardScaler()
            latent_scaled = self.scaler.fit_transform(self.latent_matrix)
        else:
            latent_scaled = self.scaler.transform(self.latent_matrix)
        
        # Apply t-SNE
        tsne = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            random_state=42,
            max_iter=1000,
            learning_rate='auto'
        )
        
        self.tsne_embeddings = tsne.fit_transform(latent_scaled)
        
        return self.tsne_embeddings
    
    def visualize_patient_clusters(self, method: str = 'both', figsize: Tuple[int, int] = (15, 6)):
        """
        Visualize patient clusters in latent space.
        
        Shows:
        - Patient similarity clusters
        - Risk categories
        - Treatment responses
        - Clinical decision boundaries
        """
        
        if method in ['pca', 'both']:
            if self.pca_embeddings is None:
                self.compute_pca_embedding()
        
        if method in ['tsne', 'both']:
            if self.tsne_embeddings is None:
                self.compute_tsne_embedding()
        
        # Create subplots
        if method == 'both':
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        else:
            fig, ax1 = plt.subplots(1, 1, figsize=(8, 6))
            ax2 = None
        
        # Color mappings
        risk_colors = {'low': 'green', 'medium': 'orange', 'high': 'red'}
        response_markers = {'good': 'o', 'poor': 's', 'adverse': '^'}
        
        # Plot PCA
        if method in ['pca', 'both']:
            for i, patient in enumerate(self.patients):
                ax1.scatter(
                    self.pca_embeddings[i, 0],
                    self.pca_embeddings[i, 1],
                    c=risk_colors[patient.risk_category],
                    marker=response_markers[patient.treatment_response],
                    s=100,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=0.5
                )
            
            ax1.set_xlabel(f'PC1 ({self.pca_model.explained_variance_ratio_[0]:.1%} variance)')
            ax1.set_ylabel(f'PC2 ({self.pca_model.explained_variance_ratio_[1]:.1%} variance)')
            ax1.set_title('PCA: Patient Latent Space\n(Linear Dimensionality Reduction)')
            ax1.grid(True, alpha=0.3)
        
        # Plot t-SNE
        if method in ['tsne', 'both'] and ax2 is not None:
            for i, patient in enumerate(self.patients):
                ax2.scatter(
                    self.tsne_embeddings[i, 0],
                    self.tsne_embeddings[i, 1],
                    c=risk_colors[patient.risk_category],
                    marker=response_markers[patient.treatment_response],
                    s=100,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=0.5
                )
            
            ax2.set_xlabel('t-SNE Dimension 1')
            ax2.set_ylabel('t-SNE Dimension 2')
            ax2.set_title('t-SNE: Patient Latent Space\n(Nonlinear Neighborhood Preservation)')
            ax2.grid(True, alpha=0.3)
        elif method == 'tsne':
            for i, patient in enumerate(self.patients):
                ax1.scatter(
                    self.tsne_embeddings[i, 0],
                    self.tsne_embeddings[i, 1],
                    c=risk_colors[patient.risk_category],
                    marker=response_markers[patient.treatment_response],
                    s=100,
                    alpha=0.7,
                    edgecolors='black',
                    linewidth=0.5
                )
            
            ax1.set_xlabel('t-SNE Dimension 1')
            ax1.set_ylabel('t-SNE Dimension 2')
            ax1.set_title('t-SNE: Patient Latent Space')
            ax1.grid(True, alpha=0.3)
        
        # Create legend
        risk_legend = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, 
                                 markersize=10, label=f'{risk.title()} Risk')
                      for risk, color in risk_colors.items()]
        
        response_legend = [plt.Line2D([0], [0], marker=marker, color='w', markerfacecolor='gray',
                                     markersize=10, label=f'{response.title()} Response')
                          for response, marker in response_markers.items()]
        
        # Add legends
        if method == 'both':
            ax1.legend(handles=risk_legend, loc='upper right', title='Risk Category')
            ax2.legend(handles=response_legend, loc='upper right', title='Treatment Response')
        else:
            ax1.legend(handles=risk_legend + response_legend, loc='upper right', 
                      title='Patient Categories')
        
        plt.tight_layout()
        plt.savefig('/Users/ryan_david_oates/cognitive-design-framework/data/patient_latent_clusters.png',
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualize_optimization_trajectories(self, patient_trajectories: Dict[str, List[np.ndarray]]):
        """
        Visualize treatment optimization trajectories in latent space.
        
        Shows:
        - Paths from initial to optimal treatment
        - Convergence patterns
        - Exploration vs exploitation regions
        """
        
        if self.pca_embeddings is None:
            self.compute_pca_embedding()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot base patient clusters
        risk_colors = {'low': 'lightgreen', 'medium': 'orange', 'high': 'lightcoral'}
        
        for i, patient in enumerate(self.patients):
            ax1.scatter(
                self.pca_embeddings[i, 0],
                self.pca_embeddings[i, 1],
                c=risk_colors[patient.risk_category],
                s=50,
                alpha=0.5
            )
            ax2.scatter(
                self.pca_embeddings[i, 0],
                self.pca_embeddings[i, 1],
                c=risk_colors[patient.risk_category],
                s=50,
                alpha=0.5
            )
        
        # Plot optimization trajectories
        trajectory_colors = ['blue', 'purple', 'brown', 'pink', 'gray']
        
        for i, (patient_id, trajectory) in enumerate(patient_trajectories.items()):
            color = trajectory_colors[i % len(trajectory_colors)]
            
            # Transform trajectory points to PCA space
            trajectory_pca = []
            for point in trajectory:
                # Transform to PCA coordinates
                point_scaled = self.scaler.transform(point.reshape(1, -1))
                point_pca = self.pca_model.transform(point_scaled)
                trajectory_pca.append(point_pca[0])
            
            trajectory_pca = np.array(trajectory_pca)
            
            # Plot trajectory
            ax1.plot(trajectory_pca[:, 0], trajectory_pca[:, 1], 
                    color=color, linewidth=2, alpha=0.8, label=f'Patient {patient_id}')
            ax1.scatter(trajectory_pca[0, 0], trajectory_pca[0, 1], 
                       color=color, marker='o', s=100, label=f'Start {patient_id}')
            ax1.scatter(trajectory_pca[-1, 0], trajectory_pca[-1, 1], 
                       color=color, marker='*', s=150, label=f'End {patient_id}')
        
        ax1.set_xlabel('PC1 (Treatment Parameter Space)')
        ax1.set_ylabel('PC2 (Treatment Parameter Space)')
        ax1.set_title('Treatment Optimization Trajectories\n(PCA Projection)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Heatmap of exploration density
        from scipy.stats import gaussian_kde
        
        if len(self.pca_embeddings) > 10:  # Need enough points for KDE
            kde = gaussian_kde(self.pca_embeddings.T)
            
            # Create grid
            x_min, x_max = self.pca_embeddings[:, 0].min(), self.pca_embeddings[:, 0].max()
            y_min, y_max = self.pca_embeddings[:, 1].min(), self.pca_embeddings[:, 1].max()
            
            xx, yy = np.meshgrid(
                np.linspace(x_min, x_max, 50),
                np.linspace(y_min, y_max, 50)
            )
            
            # Evaluate KDE
            positions = np.vstack([xx.ravel(), yy.ravel()])
            density = kde(positions).reshape(xx.shape)
            
            # Plot density
            im = ax2.contourf(xx, yy, density, levels=20, cmap='viridis', alpha=0.6)
            plt.colorbar(im, ax=ax2, label='Patient Density')
        
        ax2.set_xlabel('PC1 (Treatment Parameter Space)')
        ax2.set_ylabel('PC2 (Treatment Parameter Space)')
        ax2.set_title('Patient Density in Latent Space\n(Exploration Heatmap)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/ryan_david_oates/cognitive-design-framework/data/optimization_trajectories.png',
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def analyze_latent_space_structure(self) -> Dict[str, float]:
        """
        Analyze mathematical properties of the latent space.
        
        Returns metrics about:
        - Cluster separation
        - Dimensionality
        - Coverage
        - Optimization potential
        """
        
        if self.latent_matrix is None:
            self.encode_patients_to_latent()
        
        if self.pca_embeddings is None:
            self.compute_pca_embedding()
        
        # Compute metrics
        metrics = {}
        
        # 1. Explained variance ratio (PCA)
        metrics['pca_variance_explained'] = np.sum(self.pca_model.explained_variance_ratio_)
        
        # 2. Intrinsic dimensionality estimate
        eigenvalues = self.pca_model.explained_variance_
        metrics['intrinsic_dimensionality'] = np.sum(eigenvalues > 0.01 * eigenvalues[0])
        
        # 3. Cluster separation (silhouette-like)
        from sklearn.metrics import pairwise_distances
        
        distances = pairwise_distances(self.pca_embeddings)
        avg_intra_cluster = 0
        avg_inter_cluster = 0
        
        # Group by risk category
        risk_groups = {}
        for i, patient in enumerate(self.patients):
            if patient.risk_category not in risk_groups:
                risk_groups[patient.risk_category] = []
            risk_groups[patient.risk_category].append(i)
        
        # Compute intra-cluster distances
        intra_distances = []
        for group_indices in risk_groups.values():
            if len(group_indices) > 1:
                for i in group_indices:
                    for j in group_indices:
                        if i != j:
                            intra_distances.append(distances[i, j])
        
        # Compute inter-cluster distances
        inter_distances = []
        group_list = list(risk_groups.values())
        for i, group1 in enumerate(group_list):
            for j, group2 in enumerate(group_list):
                if i != j:
                    for idx1 in group1:
                        for idx2 in group2:
                            inter_distances.append(distances[idx1, idx2])
        
        if intra_distances and inter_distances:
            metrics['cluster_separation'] = np.mean(inter_distances) / np.mean(intra_distances)
        else:
            metrics['cluster_separation'] = 1.0
        
        # 4. Coverage (convex hull area)
        from scipy.spatial import ConvexHull
        
        try:
            hull = ConvexHull(self.pca_embeddings)
            metrics['latent_space_coverage'] = hull.volume
        except:
            metrics['latent_space_coverage'] = 0.0
        
        return metrics

def generate_demo_patients(n_patients: int = 50) -> List[PatientLatentPoint]:
    """Generate synthetic patients for latent space analysis."""
    
    np.random.seed(42)
    patients = []
    
    risk_categories = ['low', 'medium', 'high']
    responses = ['good', 'poor', 'adverse']
    
    for i in range(n_patients):
        # Generate correlated patient features
        age = np.random.normal(55, 15)
        weight = np.random.normal(75, 12)
        sex = np.random.choice(['M', 'F'])
        
        # Creatinine correlated with age
        creatinine = 0.8 + (age - 40) * 0.01 + np.random.normal(0, 0.3)
        creatinine = max(0.5, creatinine)
        
        # CYP3A4 affects metabolism
        cyp3a4_score = np.random.uniform(0.3, 1.0)
        
        # Adherence varies
        adherence = np.random.beta(8, 2)  # Skewed toward high adherence
        
        # Risk category based on age and creatinine
        if age > 70 or creatinine > 1.5:
            risk_category = np.random.choice(['medium', 'high'], p=[0.3, 0.7])
        elif age < 40 and creatinine < 1.0:
            risk_category = 'low'
        else:
            risk_category = np.random.choice(['low', 'medium'], p=[0.6, 0.4])
        
        # Treatment response based on risk and adherence
        if risk_category == 'high' or adherence < 0.7:
            response = np.random.choice(['good', 'poor', 'adverse'], p=[0.4, 0.4, 0.2])
        else:
            response = np.random.choice(['good', 'poor'], p=[0.8, 0.2])
        
        # Predicted dose
        base_dose = 5.0 * weight
        if cyp3a4_score < 0.5:  # Poor metabolizer
            predicted_dose = base_dose * 0.7
        else:
            predicted_dose = base_dose
        
        # Create latent vector (would normally come from encoder)
        latent_vector = np.random.normal(0, 1, 16)
        
        # Add patient-specific patterns
        if risk_category == 'high':
            latent_vector[:4] += np.random.normal(2, 0.5, 4)  # High-risk cluster
        elif risk_category == 'low':
            latent_vector[:4] += np.random.normal(-1, 0.5, 4)  # Low-risk cluster
        
        if response == 'adverse':
            latent_vector[4:8] += np.random.normal(3, 0.5, 4)  # Adverse response cluster
        
        patient = PatientLatentPoint(
            patient_id=f'P{i+1:03d}',
            latent_vector=latent_vector,
            clinical_features={
                'age': age,
                'weight': weight,
                'sex': sex,
                'creatinine': creatinine,
                'cyp3a4_score': cyp3a4_score,
                'adherence': adherence
            },
            predicted_dose=predicted_dose,
            actual_outcome=None,
            risk_category=risk_category,
            treatment_response=response
        )
        
        patients.append(patient)
    
    return patients

def main():
    """Demonstrate latent space analysis for medical AI."""
    
    print("🧬 Latent Space Analysis for Medical AI Ensemble Systems")
    print("=" * 70)
    print("Mathematical Framework: PCA + t-SNE for Patient Parameter Visualization")
    print()
    
    # Generate demo patients
    print("1. Generating synthetic patient cohort...")
    patients = generate_demo_patients(50)
    print(f"   Created {len(patients)} patients with diverse characteristics")
    
    # Initialize analyzer
    analyzer = MedicalLatentSpaceAnalyzer()
    
    # Add patients
    for patient in patients:
        analyzer.add_patient(patient)
    
    print("2. Encoding patients to latent space...")
    latent_matrix = analyzer.encode_patients_to_latent()
    print(f"   Latent matrix shape: {latent_matrix.shape} (patients × latent_dim)")
    
    print("3. Computing dimensionality reductions...")
    pca_embeddings = analyzer.compute_pca_embedding()
    tsne_embeddings = analyzer.compute_tsne_embedding()
    print(f"   PCA embeddings: {pca_embeddings.shape}")
    print(f"   t-SNE embeddings: {tsne_embeddings.shape}")
    
    print("4. Visualizing patient clusters...")
    analyzer.visualize_patient_clusters(method='both')
    
    print("5. Analyzing latent space structure...")
    metrics = analyzer.analyze_latent_space_structure()
    
    print("   Latent Space Metrics:")
    for metric, value in metrics.items():
        print(f"     {metric}: {value:.4f}")
    
    print()
    print("6. Generating optimization trajectories...")
    
    # Create sample optimization trajectories
    trajectories = {}
    for i in range(3):
        patient = patients[i]
        # Simulate optimization path in latent space
        start = patient.latent_vector.copy()
        trajectory = [start]
        
        # Simulate 5 optimization steps
        current = start.copy()
        for step in range(5):
            # Move toward better region (simplified)
            if patient.risk_category == 'high':
                direction = np.random.normal(-0.2, 0.1, len(current))  # Move toward low-risk
            else:
                direction = np.random.normal(0, 0.05, len(current))  # Small adjustments
            
            current = current + direction
            trajectory.append(current.copy())
        
        trajectories[patient.patient_id] = trajectory
    
    analyzer.visualize_optimization_trajectories(trajectories)
    
    print("✅ Latent space analysis completed!")
    print()
    print("🎯 Key Insights:")
    print("   • Patient clusters reveal risk-based groupings")
    print("   • t-SNE preserves local neighborhood structure")
    print("   • PCA shows global variance patterns")
    print("   • Optimization trajectories guide treatment paths")
    print("   • Unexplored regions suggest new patient types")
    print()
    print("📊 Clinical Applications:")
    print("   • Patient similarity matching for treatment selection")
    print("   • Risk stratification visualization")
    print("   • Treatment optimization path planning")
    print("   • Novel patient phenotype discovery")
    print("   • Model ensemble behavior analysis")

if __name__ == "__main__":
    main()
