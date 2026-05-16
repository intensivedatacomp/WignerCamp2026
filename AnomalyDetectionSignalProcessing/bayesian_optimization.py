from skopt import BayesSearchCV
from skopt.space import Real, Categorical
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)

#|%%--%%| <3dJJ805LHw|GraSsYP98b>
# ==============================================================
# Single-parameter search: tuning C of LogisticRegression
# ==============================================================

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf',    LogisticRegression(max_iter=1000))
])

opt = BayesSearchCV(
    estimator=pipe,
    search_spaces={'clf__C': Real(1e-3, 1e2, prior='log-uniform')},
    n_iter=20,
    cv=5,
    scoring='accuracy',
    random_state=42
)
opt.fit(X, y)

print("=== Single-parameter search: LogisticRegression ===")
print(f"Best C:     {opt.best_params_['clf__C']:.4f}")
print(f"Best score: {opt.best_score_:.4f}")
print()
print("All evaluated configurations:")
for params, score in zip(opt.cv_results_['params'],
                         opt.cv_results_['mean_test_score']):
    print(f"  {params} -> {score:.4f}")

#|%%--%%| <GraSsYP98b|2TsALmBImJ>
# ==============================================================
# Multi-parameter search: tuning C, gamma, kernel of SVC
# ==============================================================

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc',    SVC())
])

opt = BayesSearchCV(
    estimator=pipe,
    search_spaces={
        'svc__C':      Real(1e-2, 1e2,  prior='log-uniform'),
        'svc__gamma':  Real(1e-4, 1e-1, prior='log-uniform'),
        'svc__kernel': Categorical(['rbf', 'poly'])
    },
    n_iter=40,
    cv=5,
    scoring='accuracy',
    random_state=42
)
opt.fit(X, y)

print()
print("=== Multi-parameter search: SVC ===")
print(f"Best params: {dict(opt.best_params_)}")
print(f"Best score:  {opt.best_score_:.4f}")
