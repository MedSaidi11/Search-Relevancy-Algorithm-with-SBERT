pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'prod', url: 'https://github.com/MedSaidi11/Semantic-Search-Engine-using-Sentence-BERT.git'
            }
        }
        
        stage('Restart EC2 Instance') {
            steps {
                withCredentials([
                    string(credentialsId: 'INSTANCE_ID', variable: 'EC2_INSTANCE_ID'),
                    string(credentialsId: 'AWS_REGION', variable: 'AWS_REGION'),
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'SECRET-ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    script {
                        sh """
                            aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                            aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                            aws configure set default.region $AWS_REGION

                            echo "Rebooting EC2 instance with ID: $EC2_INSTANCE_ID in region: $AWS_REGION"
                            aws ec2 reboot-instances --instance-ids $EC2_INSTANCE_ID --region $AWS_REGION
                        """
                    }
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
                        docker-compose up -d
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
