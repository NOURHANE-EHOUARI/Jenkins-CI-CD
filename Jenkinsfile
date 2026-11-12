pipeline {
    agent any

    environment {
        GITHUB_TOKEN = credentials('github-token')
        VENV_DIR     = '.venv'
        HOST         = '0.0.0.0'
        PORT         = '5000'
        APP_MODULE   = 'app:app'
    }

    // Part 5: build every 5 minutes (cron) and on every GitHub push (webhook)
    triggers {
        cron('H/5 * * * *')
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the code from GitHub (branch main) using the GitHub credentials
                git branch: 'main',
                    url: 'https://github.com/NOURHANE-EHOUARI/Jenkins-CI-CD.git',
                    credentialsId: 'github-token'
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                // Create the Python virtual environment and install the dependencies
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt pytest-cov
                    python --version
                '''
            }
        }

        stage('Run Tests') {
            steps {
                // Run the tests with pytest and generate a coverage report
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p reports
                    python -m pytest test_app.py -v \
                        --cov=app --cov-report=term-missing --cov-report=xml:reports/coverage.xml \
                        --junitxml=reports/test_app.xml
                '''
            }
            post {
                always {
                    // Display the test results in Jenkins and keep the reports
                    junit 'reports/test_*.xml'
                    archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                // Start the app locally with gunicorn (stop the previous instance first)
                sh '''
                    . ${VENV_DIR}/bin/activate
                    if [ -f gunicorn.pid ]; then kill $(cat gunicorn.pid) || true; sleep 1; fi
                    JENKINS_NODE_COOKIE=dontKillMe nohup gunicorn --bind ${HOST}:${PORT} ${APP_MODULE} \
                        --pid gunicorn.pid > gunicorn.log 2>&1 &
                    sleep 3
                    cat gunicorn.log
                    echo "App deployed on http://localhost:${PORT}"
                '''
            }
        }
    }
}
