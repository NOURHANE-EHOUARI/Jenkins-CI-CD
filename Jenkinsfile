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
            // Part 6: run the two test files in parallel
            parallel {
                stage('Tests test_app.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            mkdir -p reports
                            COVERAGE_FILE=.coverage.app1 python -m pytest test_app.py -v \
                                --cov=app --cov-report=term-missing --cov-report=xml:reports/coverage_app.xml \
                                --junitxml=reports/test_app.xml
                        '''
                    }
                    post {
                        always {
                            junit 'reports/test_app.xml'
                        }
                    }
                }
                stage('Tests test_app_2.py') {
                    steps {
                        sh '''
                            . ${VENV_DIR}/bin/activate
                            mkdir -p reports
                            COVERAGE_FILE=.coverage.app2 python -m pytest test_app_2.py -v \
                                --cov=app --cov-report=term-missing --cov-report=xml:reports/coverage_app_2.xml \
                                --junitxml=reports/test_app_2.xml
                        '''
                    }
                    post {
                        always {
                            junit 'reports/test_app_2.xml'
                        }
                    }
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
