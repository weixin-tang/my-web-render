// 表单提交处理
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFormSubmit);
    }
});

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        title: formData.get('title') || null,
        html_content: formData.get('html_content')
    };
    
    try {
        const response = await fetch('/web-render/api/pages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess(result);
            event.target.reset();
        } else {
            showError(result.detail || '创建失败');
        }
    } catch (error) {
        showError('网络错误：' + error.message);
    }
}

function showSuccess(result) {
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const pageUrl = document.getElementById('pageUrl');
    const previewUrl = document.getElementById('previewUrl');
    
    const fullUrl = window.location.origin + '/web-render' + result.url;
    const fullPreviewUrl = window.location.origin + '/web-render/preview/' + result.page_id;
    
    pageUrl.href = fullUrl;
    pageUrl.textContent = fullUrl;
    previewUrl.href = fullPreviewUrl;
    previewUrl.textContent = fullPreviewUrl;
    
    errorDiv.style.display = 'none';
    resultDiv.style.display = 'block';
}

function showError(message) {
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'block';
}

// 删除页面
async function deletePage(pageId) {
    if (!confirm('确定要删除这个网页吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`/web-render/api/pages/${pageId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('删除成功');
            window.location.reload();
        } else {
            const result = await response.json();
            alert('删除失败：' + (result.detail || '未知错误'));
        }
    } catch (error) {
        alert('网络错误：' + error.message);
    }
}

// 复制链接到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('链接已复制到剪贴板');
    }, function(err) {
        console.error('复制失败: ', err);
    });
}