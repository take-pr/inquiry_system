document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript が正常に読み込まれました！");

    // 🔹 タスクのドラッグ&ドロップ（カンバン方式）
    const taskColumns = document.querySelectorAll(".task-column");
    let draggedTask = null;

    document.querySelectorAll(".task-item").forEach(task => {
        task.draggable = true;
        task.addEventListener("dragstart", function () {
            draggedTask = task;
        });
    });

    taskColumns.forEach(column => {
        column.addEventListener("dragover", function (event) {
            event.preventDefault();
        });
        column.addEventListener("drop", function () {
            if (draggedTask) {
                column.appendChild(draggedTask);
                updateTaskStatus(draggedTask.dataset.taskId, column.dataset.status);
                draggedTask = null;
            }
        });
    });

    function updateTaskStatus(taskId, newStatus) {
        fetch(`/tasks/${taskId}/update-status/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ status: newStatus })
        }).then(response => response.json()).then(data => {
            console.log("✅ タスク更新成功:", data);
        }).catch(error => {
            console.error("❌ タスク更新エラー:", error);
        });
    }

    function getCSRFToken() {
        const tokenElement = document.querySelector("input[name='csrfmiddlewaretoken']");
        return tokenElement ? tokenElement.value : "";
    }

    // 🔹 締め切りが近いタスクの通知
    document.querySelectorAll(".task-item").forEach(task => {
        const deadlineStr = task.dataset.deadline;
        
        if (!deadlineStr) {
            console.warn("⚠ 締め切りが設定されていないタスク:", task.textContent);
            return;
        }

        const deadline = new Date(deadlineStr);
        const today = new Date();
        const timeDiff = (deadline - today) / (1000 * 60 * 60 * 24);

        console.log(`📅 タスク: ${task.textContent}, 期限: ${deadline.toDateString()}, 残り日数: ${timeDiff}`);

        if (timeDiff <= 3 && timeDiff >= 0) {
            task.style.backgroundColor = "#ffcccc"; 
            showNotification(`⚠ 締め切りが近いタスク: ${task.textContent}`);
        }
    });

    function showNotification(message) {
        const notification = document.createElement("div");
        notification.classList.add("notification");
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
});
