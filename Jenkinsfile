pipeline {
    agent any

    environment {
        EC2_INSTANCE_ID = credentials("INSTANCE_ID")
        AWS_REGION = credentials("AWS_REGION")     
        AWS_ACCESS_KEY_ID = credentials("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = credentials("SECRET-ACCESS_KEY")
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'prod', url: 'https://github.com/MedSaidi11/Semantic-Search-Engine-using-Sentence-BERT.git'
            }
        }

        stage('Print Environment Variables') {
            steps {
                script {
                    // Printing only non-sensitive environment variables for debugging
                    echo "AWS_REGION: $AWS_REGION"
                    echo "EC2_INSTANCE_ID: $EC2_INSTANCE_ID"
                    // Avoid printing AWS Access Keys as they are sensitive
                }
            }
        }

        stage('Restart EC2 Instance') {
            steps {
                script {
                    // Use AWS CLI to restart EC2 instance
                    sh """
                        aws ec2 reboot-instances --instance-ids $EC2_INSTANCE_ID --region $AWS_REGION
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        docker-compose build
                    """
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh """
                        docker-compose up
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Build and deployment successful.'
        }
        failure {
            echo 'There was a failure in the pipeline.'
        }
    }
}
