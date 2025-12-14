import requests

# 测试保存工作流接口
def test_create_workflow():
    url = "http://localhost:8000/api/v1/workflows/"
    
    # 示例数据
    workflow_data = {
        "name": "Test Workflow",
        "description": "This is a test workflow"
    }
    
    try:
        response = requests.post(url, json=workflow_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error calling API: {str(e)}")

if __name__ == "__main__":
    test_create_workflow()